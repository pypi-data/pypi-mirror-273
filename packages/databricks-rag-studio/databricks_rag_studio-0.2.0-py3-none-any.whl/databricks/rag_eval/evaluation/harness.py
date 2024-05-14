"""Entry point to the evaluation harness"""

from __future__ import annotations

import itertools
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partialmethod
from typing import List, Optional

import mlflow
from tqdm.auto import tqdm

from databricks.rag_eval import env_vars
from databricks.rag_eval.config import assessment_config, judge_config
from databricks.rag_eval.config import evaluation_config
from databricks.rag_eval.evaluation import (
    assessments,
    entities,
    summary,
    models,
)
from databricks.rag_eval.evaluation.assessments import llm_proxy_monkey_patch
from databricks.rag_eval.utils import rate_limit


def run(
    *,
    eval_items: List[entities.EvalItem],
    config: evaluation_config.EvaluationConfig,
    model: Optional[mlflow.pyfunc.PyFuncModel] = None,
) -> List[entities.EvalResult]:
    """
    Run the logic of the eval harness.

    :param eval_items: List of EvalItems
    :param config: The evaluation config
    :param model: Optional model to use for generating responses and traces
    """
    # Disable tqdm progress bar by default so that the progress bars inside MLflow eval_fn do not show
    tqdm.__init__ = partialmethod(tqdm.__init__, disable=True)

    assessments_to_run: List[assessments.Assessment] = list(
        itertools.chain.from_iterable(
            _get_assessments_for_llm_judge(assessment_judge)
            for assessment_judge in config.assessment_judges
        )
    )
    eval_results = []
    # Patch the mlflow.metrics.genai.model_utils to support model endpoints in the form of "llmproxy:/gpt-4" using
    # the LlmProxy mlflow deployment plugin
    # This patch should be applied outside the ThreadPoolExecutor because the patch is not thread-safe
    with llm_proxy_monkey_patch():
        with ThreadPoolExecutor(
            max_workers=env_vars.RAG_EVAL_MAX_WORKERS.get()
        ) as executor:
            futures = [
                executor.submit(
                    _run_single,
                    eval_item=eval_item,
                    assessments_to_run=assessments_to_run,
                    model=model,
                )
                for eval_item in eval_items
            ]

            futures_as_completed = as_completed(futures)
            # Add a progress bar to show the progress of the assessments
            futures_as_completed = tqdm(
                futures_as_completed,
                total=len(futures),
                disable=False,
                desc="Evaluating",
            )

            for future in futures_as_completed:
                result = future.result()
                eval_results.append(result)
        return eval_results


def _run_single(
    eval_item: entities.EvalItem,
    assessments_to_run: List[assessments.Assessment],
    model: Optional[mlflow.pyfunc.PyFuncModel] = None,
) -> entities.EvalResult:
    """
    Run the logic of the eval harness for a single eval item.

    :param eval_item: The eval item to evaluate
    :param assessments_to_run: The list of assessments to run
    :param model: Optional model to use for generating responses and traces
    """
    if model:
        eval_item = _populate_model_result_to_eval_item(
            eval_item=eval_item,
            model_result=models.invoke_model(model, eval_item),
        )
    assessment_log = assessments.generate_llm_assessments(
        eval_item=eval_item,
        assessments=assessments_to_run,
    )
    return summary.generate_eval_summary(assessment_log)


def _populate_model_result_to_eval_item(
    eval_item: entities.EvalItem, model_result: models.ModelResult
) -> entities.EvalItem:
    """
    Populate the model result to the eval item.

    :param eval_item: The eval item to populate the model result
    :param model_result: The model result to populate
    :return: The populated eval item
    """
    # TODO[ML-39624]: figure out a good way to surface the error message from invoking the model
    return entities.EvalItem(
        question_id=eval_item.question_id,
        question=eval_item.question,
        ground_truth_answer=eval_item.ground_truth_answer,
        ground_truth_retrieval_context=eval_item.ground_truth_retrieval_context,
        answer=model_result.response,
        retrieval_context=model_result.retrieval_context,
        trace=model_result.trace,
    )


def _get_assessments_for_llm_judge(
    assessment_judge: judge_config.AssessmentJudge,
) -> List[assessments.Assessment]:
    """
    Construct a list of assessments for a single LLM judge.

    :param assessment_judge: The LLM judge to generate assessments
    :return: A list of assessments
    """
    source = assessment_config.AssessmentSource(
        source_id=assessment_judge.judge_name,
        model=assessment_judge.endpoint_name,
        rate_limiter=_build_rate_limiter_for_assessment(),
    )

    return [
        (
            assessments.BuiltInAssessment(
                config=config, source=source, examples=examples
            )
            if isinstance(config, assessment_config.BuiltinAssessmentConfig)
            else assessments.CustomAssessment(
                config=config, source=source, examples=examples
            )
        )
        for config, examples in assessment_judge.assessment_configs_and_examples.items()
    ]


def _build_rate_limiter_for_assessment() -> rate_limit.RateLimiter:
    """Build a rate limiter for the assessment."""
    # Return a no-op rate limiter if the rate limiter for assessment is not enabled
    if not env_vars.RAG_EVAL_ENABLE_RATE_LIMIT_FOR_ASSESSMENT.get():
        return rate_limit.RateLimiter.no_op()

    # For now, rate limiter config is from environment variables
    rate_limit_config = assessment_config.RateLimitConfig(
        quota=env_vars.RAG_EVAL_RATE_LIMIT_QUOTA.get(),
        time_window_in_seconds=env_vars.RAG_EVAL_RATE_LIMIT_TIME_WINDOW_IN_SECONDS.get(),
    )
    return rate_limit.RateLimiter.build(
        quota=rate_limit_config.quota,
        time_window_in_seconds=rate_limit_config.time_window_in_seconds,
    )
