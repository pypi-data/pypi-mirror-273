import abc
import dataclasses
import numbers
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from inspect import signature
from typing import List, Collection, Optional, Any

import pandas as pd
from mlflow.deployments import set_deployments_target
from mlflow.metrics import MetricValue
from mlflow.metrics.genai import EvaluationExample
from mlflow.models import EvaluationMetric

from databricks.rag_eval import constants
from databricks.rag_eval.config import (
    example_config,
    assessment_config,
    constants as config_constants,
)
from databricks.rag_eval.context import context
from databricks.rag_eval.evaluation import entities
from databricks.rag_eval.judges import (
    constants as judge_constants,
    custom_judges,
)
from databricks.rag_eval.utils import collection_utils


@dataclasses.dataclass(frozen=True)
class Assessment(abc.ABC):
    """
    Assessment represents a method to assess the quality of a RAG system.
    """

    @abc.abstractmethod
    def run(self, eval_item: entities.EvalItem) -> List[entities.AssessmentResult]:
        """
        Run the assessment on a single eval item and produce a list of assessment results.
        A single eval item can produce multiple assessment results since multiple assessments can be batch computed
        together for a single EvalItem.

        If the eval item does not have required fields for the assessment, return an empty list.

        :param eval_item: The eval item to assess.
        :return: A list of assessment results.
        """
        pass


@dataclasses.dataclass(frozen=True)
class BuiltInAssessment(Assessment):
    """
    This implementation uses = the LLM judge service to compute the assessments
    """

    config: assessment_config.AssessmentConfig
    """
    Static configuration for the assessment. 
    Can be user-provided for custom assessments.
    """
    source: assessment_config.AssessmentSource
    """
    Source of the assessment.
    This is used to identify the source of the assessment in the assessment log.
    """
    examples: List[example_config.AssessmentExample] = dataclasses.field(
        default_factory=list
    )

    def run(self, eval_item: entities.EvalItem) -> List[entities.AssessmentResult]:
        llm_judge_client = context.llm_judge_client
        assessment_name = self.config.assessment_name
        with self.source.rate_limiter:
            result = llm_judge_client.get_assessment(
                eval_item,
                assessment_name,
                self.config.assessment_type,
                self.examples,
            )
            return result


@dataclasses.dataclass(frozen=True)
class MlflowAssessment(Assessment):
    """
    Assessment that uses Mlflow EvaluationMetric abstraction.
    """

    config: assessment_config.BuiltinAssessmentConfig
    """
    Static configuration for the assessment.
    Can be user-provided for custom assessments.
    """
    source: assessment_config.AssessmentSource
    """
    Source of the assessment.
    This is used to identify the source of the assessment in the assessment log.
    """
    examples: List[example_config.AssessmentExample] = dataclasses.field(
        default_factory=list
    )

    @property
    def name(self):
        return self.config.assessment_name

    @property
    def assessment_type(self):
        return self.config.assessment_type

    def run(self, eval_item: entities.EvalItem) -> List[entities.AssessmentResult]:
        # Note: this lets us call the Databricks endpoints.
        set_deployments_target("databricks")

        if not _eval_item_has_required_fields(eval_item, self.config):
            return []

        match self.assessment_type:
            case assessment_config.AssessmentType.RETRIEVAL:
                return [self._run_retrieval_assessment(eval_item)]
            case assessment_config.AssessmentType.ANSWER:
                return [self._run_answer_assessment(eval_item)]
            case _:
                raise ValueError(
                    f"Assessment type '{self.assessment_type}' is not supported."
                    f"Supported types are: {assessment_config.AssessmentType.ANSWER} and {assessment_config.AssessmentType.RETRIEVAL}."
                )

    def _run_answer_assessment(
        self, eval_item: entities.EvalItem
    ) -> entities.AnswerAssessmentResult:
        """
        Run the answer assessment on the eval item and produce an answer assessment result.
        """
        eval_metric = self.load_metric()
        with self.source.rate_limiter:
            mlflow_metric_value: MetricValue = self._compute_answer_metric_value(
                eval_metric, eval_item
            )

        rating = _mlflow_eval_value_to_rating(
            mlflow_metric_value, self.config.binary_conversion
        )
        return entities.AnswerAssessmentResult(
            assessment_name=self.name,
            rating=rating,
        )

    def _run_retrieval_assessment(
        self, eval_item: entities.EvalItem
    ) -> entities.RetrievalAssessmentResult:
        """
        Run the retrieval assessment on the eval item and produce a retrieval assessment result.

        The retrieval assessment is a positional assessment, where each position in the retrieval context
        is rated separately.
        """
        positional_ratings = {}
        eval_metric = self.load_metric()
        for pos, chunk in enumerate(eval_item.retrieval_context):
            # Skip the chunk if it is empty
            if chunk is None or not chunk.content:
                continue

            mlflow_metric_value: MetricValue = self._compute_retrieval_metric_value(
                eval_metric, eval_item, chunk, pos
            )

            rating = _mlflow_eval_value_to_rating(
                mlflow_metric_value, self.config.binary_conversion
            )
            positional_ratings[pos] = rating

        return entities.RetrievalAssessmentResult(
            assessment_name=self.name,
            positional_rating=positional_ratings,
        )

    @abc.abstractmethod
    def load_metric(self) -> EvaluationMetric:
        """
        Loads the Mlflow EvaluationMetric object.
        """
        pass

    @abc.abstractmethod
    def get_eval_fn_params(self) -> List[str]:
        """
        Get a list of parameter names needed for the eval_fn of the metric.
        """
        pass

    @abc.abstractmethod
    def _compute_retrieval_metric_value(
        self,
        eval_metric: EvaluationMetric,
        eval_item: entities.EvalItem,
        chunk: entities.Chunk,
        pos: int,
    ) -> MetricValue:
        """
        Compute a mlflow MetricValue for a retrieval assessment given the EvalItem, input chunk and position
        """
        pass

    @abc.abstractmethod
    def _compute_answer_metric_value(
        self, eval_metric: EvaluationMetric, eval_item: entities.EvalItem
    ) -> MetricValue:
        """
        Compute a mlflow MetricValue for an answer assessment given the EvalItem
        """
        pass


@dataclasses.dataclass(frozen=True)
class LegacyBuiltInAssessment(MlflowAssessment):
    """
    The legacy assessment that uses a built-in Mlflow EvaluationMetric.

    :param config: The configuration for the assessment.
    :param source: The source of the assessment.
    :param examples: The examples for the assessment.
    """

    config: assessment_config.BuiltinAssessmentConfig

    def load_metric(self) -> EvaluationMetric:
        # Get path to of the metric module to import by name
        module_parts = self.config.module_path.split(".")
        module_name = ".".join(module_parts[:-1])
        class_name = module_parts[-1]
        module = __import__(module_name, fromlist=[class_name])
        metric_class = getattr(module, class_name)
        # Construct the MLflow EvaluationMetric object with the given metric args.
        # The args in the config take precedence over the common args defined here.
        metric_args = {
            constants.METRIC_ARG_KEY__MODEL: self.source.model,
            # If no examples, use None so as not to override built-in examples in the mlflow evaluation class
            constants.METRIC_ARG_KEY__EXAMPLES: _construct_mlflow_examples_for_builtin_assessment(
                self.config, self.examples
            )
            or None,
            **self.config.args,
        }
        return metric_class(**metric_args)

    def get_eval_fn_params(self) -> List[str]:
        """
        Get a list of parameter names needed for the eval_fn of the metric.
        """
        eval_metric = self.load_metric()
        return list(signature(eval_metric.eval_fn).parameters.keys())

    def _compute_answer_metric_value(
        self, eval_metric: EvaluationMetric, eval_item: entities.EvalItem
    ) -> MetricValue:
        eval_fn_input_params = list(signature(eval_metric.eval_fn).parameters.keys())
        eval_fn_args = [
            pd.Series([_extract_mlflow_eval_fn_args(eval_item, param)])
            for param in eval_fn_input_params
        ]
        # Rate limit the request to the built-in assessment LLM judge model
        with self.source.rate_limiter:
            mlflow_metric_value: MetricValue = eval_metric.eval_fn(*eval_fn_args)

        return mlflow_metric_value

    def _compute_retrieval_metric_value(
        self,
        eval_metric: EvaluationMetric,
        eval_item: entities.EvalItem,
        chunk: entities.Chunk,
        pos: int,
    ) -> MetricValue:
        eval_fn_input_params = list(signature(eval_metric.eval_fn).parameters.keys())
        # Assuming "retrieved_content" is from the chunk content for each chunk in the retrieval context
        # and other params are extracted from eval_item
        eval_fn_args = [
            (
                pd.Series([chunk.content])
                if param == judge_constants.RETRIEVED_CONTENT
                else pd.Series([_extract_mlflow_eval_fn_args(eval_item, param)])
            )
            for param in eval_fn_input_params
        ]
        # Rate limit the request to the built-in assessment LLM judge model
        with self.source.rate_limiter:
            mlflow_metric_value: MetricValue = eval_metric.eval_fn(*eval_fn_args)

        return mlflow_metric_value


@dataclasses.dataclass(frozen=True)
class CustomAssessment(MlflowAssessment):
    """
    Assessment that uses MLflow EvaluationMetric.
    """

    config: assessment_config.CustomAssessmentConfig

    def load_metric(self) -> EvaluationMetric:
        return custom_judges.make_custom_genai_metric(
            assessment_conf=self.config,
            model=self.source.model,
            examples=self.examples,
            # Support only greater is better for now
            greater_is_better=True,
        )

    def get_eval_fn_params(self) -> List[str]:
        raise ValueError(
            "get_eval_fn_params not supported for non-builtin assessment config type"
        )

    def _compute_answer_metric_value(
        self, eval_metric: EvaluationMetric, eval_item: entities.EvalItem
    ) -> MetricValue:
        with self.source.rate_limiter:
            mlflow_metric_value: MetricValue = eval_metric.eval_fn(eval_item)

        return mlflow_metric_value

    def _compute_retrieval_metric_value(
        self,
        eval_metric: EvaluationMetric,
        eval_item: entities.EvalItem,
        chunk: entities.Chunk,
        pos: int,
    ) -> MetricValue:
        with self.source.rate_limiter:
            mlflow_metric_value: MetricValue = eval_metric.eval_fn(
                eval_item, chunk_pos=pos
            )
        return mlflow_metric_value


def generate_llm_assessments(
    *, eval_item: entities.EvalItem, assessments: List[Assessment]
) -> entities.AssessmentLog:
    """
    Performs the LLM judged assessment on a EvalItems and generates a AssessmentLog
    using the given LLM judge model and assessments.

    The method only uses the compatible assessments for the given eval dataset.
    An assessment is incompatible if it requires extra information which is missing in the eval item.
    For example, an assessment is not compatible if it requires retrieval context
    but the eval dataset does not have retrieval context.

    :param eval_item: The eval item to evaluate on.
    :param assessments: The list of assessments to use.
    """
    if not assessments:
        return entities.AssessmentLog(eval_item=eval_item, assessment_results=[])

    assessment_results: List[entities.AssessmentResult] = []
    # Use a thread pool to run assessments in parallel
    # Use the number of assessments as the number of workers
    with ThreadPoolExecutor(max_workers=len(assessments)) as executor:
        futures = [
            executor.submit(
                _run_assessment,
                eval_item=eval_item,
                assessment=assessment,
            )
            for assessment in assessments
        ]

        for future in as_completed(futures):
            result = future.result()
            assessment_results.extend(result)

    return entities.AssessmentLog(
        eval_item=eval_item,
        assessment_results=assessment_results,
    )


def _run_assessment(
    eval_item: entities.EvalItem,
    assessment: Assessment,
) -> List[entities.AssessmentResult]:
    """
    Run the assessment on a single eval item and produce a list of assessment results.
    """
    return assessment.run(eval_item)


# TODO(ML-39566): the monkey patch is quite brittle as it relies on private methods, work with mlflow team to find a better way
@contextmanager
def llm_proxy_monkey_patch():
    """
    Monkey patch the mlflow.metrics.genai.model_utils to support model endpoints in the form of "llmproxy:/gpt-4"

    The patch is done in two places:
    1. allow the "llmproxy" prefix to be treated just like a standard deployment plugin
    2. allow mlflow to resolve the LLM proxy deployment plugin by patching get_deploy_client() with target_uri="llmproxy"

    Wrapping this around a contextmanager so that we can revert back to the original methods so that non LLM proxy
    use cases go through the original code path
    """

    from mlflow.metrics.genai import model_utils
    from mlflow.metrics.genai.model_utils import _parse_model_uri, _call_deployments_api
    from mlflow import deployments

    original_score_model_on_payload = model_utils.score_model_on_payload
    original_get_deploy_client = deployments.get_deploy_client

    def patched_score_model_on_payload(model_uri, payload, eval_parameters=None):
        eval_parameters = eval_parameters or {}

        prefix, suffix = _parse_model_uri(model_uri)

        deployments.get_deploy_client = lambda plugin=None: (
            original_get_deploy_client("llmproxy")
            if prefix == "llmproxy"
            else original_get_deploy_client()
        )
        if prefix == "llmproxy":
            return _call_deployments_api(suffix, payload, eval_parameters)
        else:
            return original_score_model_on_payload(model_uri, payload, eval_parameters)

    model_utils.score_model_on_payload = patched_score_model_on_payload

    try:
        yield
    finally:
        model_utils.score_model_on_payload = original_score_model_on_payload
        deployments.get_deploy_client = original_get_deploy_client


def _rename_input_dict_for_builtin_assessment(
    assessment_conf: assessment_config.AssessmentConfig,
    example: example_config.AssessmentExample,
) -> dict[str, str]:
    """
    Rename variables in the example according to mlflow's expectations.
    The example will be validated upstream in config creation,
    so we can assume the required fields are present based on the assessment conf.

    This overwrites duplicate values. For instance, if the user provides an extraneous `response` column for
    chunk_relevance but also provides the required `context` column (to be renamed to `response`), the
    extraneous `response` column will be overwritten.
    """
    # Import here to avoid circular import
    from databricks.rag_eval.judges import builtin_judge

    variables_dict = dict(example.variables)

    if assessment_conf == builtin_judge.CHUNK_RELEVANCE:
        # the context should be the "response" for this assessment
        variables_dict[config_constants.ALLOWED_PROMPT_VARIABLE__RESPONSE] = (
            variables_dict.pop(config_constants.ALLOWED_PROMPT_VARIABLE__CONTEXT)
        )

    if config_constants.ALLOWED_PROMPT_VARIABLE__EXPECTED_RESPONSE in variables_dict:
        variables_dict["targets"] = variables_dict.pop(
            config_constants.ALLOWED_PROMPT_VARIABLE__EXPECTED_RESPONSE
        )

    return variables_dict


def _construct_mlflow_examples_for_builtin_assessment(
    assessment_conf: assessment_config.AssessmentConfig,
    examples: Collection[example_config.AssessmentExample],
) -> List[EvaluationExample]:
    binary_converter = assessment_config.BinaryConversion(
        threshold=5.0, greater_is_true=True
    )
    mlflow_examples = []

    for example in examples:
        remapped_example_variables = _rename_input_dict_for_builtin_assessment(
            assessment_conf, example
        )

        grading_context = collection_utils.omit_keys(
            remapped_example_variables,
            [
                config_constants.ALLOWED_PROMPT_VARIABLE__REQUEST,
                config_constants.ALLOWED_PROMPT_VARIABLE__RESPONSE,
            ],
        )

        mlflow_examples.append(
            EvaluationExample(
                input=remapped_example_variables.get(
                    config_constants.ALLOWED_PROMPT_VARIABLE__REQUEST, None
                ),
                output=remapped_example_variables.get(
                    config_constants.ALLOWED_PROMPT_VARIABLE__RESPONSE, None
                ),
                score=binary_converter.convert_to_score(example.value),
                justification=example.rationale or "",
                grading_context=grading_context,
            )
        )

    return mlflow_examples


def _eval_item_has_required_fields(
    eval_item: entities.EvalItem, assessment_config: assessment_config.AssessmentConfig
) -> bool:
    """
    Check if the eval item has the required fields for the assessment.
    """
    if assessment_config.require_answer and eval_item.answer is None:
        return False
    if (
        assessment_config.require_retrieval_context
        and eval_item.concatenated_retrieval_context is None
    ):
        return False
    if (
        assessment_config.require_retrieval_context_array
        and eval_item.retrieval_context is None
    ):
        return False
    if (
        assessment_config.require_ground_truth_answer
        and eval_item.ground_truth_answer is None
    ):
        return False
    return True


def _extract_mlflow_eval_fn_args(eval_item: entities.EvalItem, param: str) -> Any:
    """
    Extract the value of eval_fn arguments from the eval item given the param name.

    Param name should be in sync with the signature of the eval_fn in MLflow.
    """
    match param:
        case judge_constants.MLFLOW_EVAL_FN_INPUTS:
            return eval_item.question
        case judge_constants.MLFLOW_EVAL_FN_METRICS:
            return ""
        case judge_constants.MLFLOW_EVAL_FN_PREDICTIONS:
            return eval_item.answer
        case judge_constants.MLFLOW_EVAL_FN_CONTEXT:
            return eval_item.concatenated_retrieval_context
        case judge_constants.MLFLOW_EVAL_FN_TARGETS:
            return eval_item.ground_truth_answer


def _mlflow_eval_value_to_rating(
    mlflow_metric_value: Optional[MetricValue],
    binary_conversion: Optional[assessment_config.BinaryConversion],
) -> entities.Rating:
    """
    Convert the MLflow metric value to a Rating object.
    Assumes that the MLflow metric value only contains results for a single row.
    """
    # Return error rating if the scores or justifications are empty
    if (
        mlflow_metric_value is None
        or mlflow_metric_value.scores is None
        or len(mlflow_metric_value.scores) == 0
        or mlflow_metric_value.justifications is None
        or len(mlflow_metric_value.justifications) == 0
    ):
        return entities.Rating.error(
            f"Fail to get the assessment result: {mlflow_metric_value}"
        )

    # Assume that the scores and justifications are for a single row
    assert (
        len(mlflow_metric_value.scores) == 1
    ), f"Expected a single score, but got {len(mlflow_metric_value.scores)} scores."
    score = mlflow_metric_value.scores[0]
    justification = mlflow_metric_value.justifications[0]

    if score is None:
        # If the score is None, it means there is as an error.
        # In this case, the error message is the justification.
        return entities.Rating.error(justification)

    if not isinstance(score, numbers.Real):
        # If the score is not a real number, we treat it as an error.
        return entities.Rating.error(
            f"Could not extract numerical score from '{score}': {justification}"
        )
    else:
        return entities.Rating.build(
            bool_value=(
                binary_conversion.convert(score) if binary_conversion else None
            ),
            double_value=float(score),
            rationale=justification,
        )
