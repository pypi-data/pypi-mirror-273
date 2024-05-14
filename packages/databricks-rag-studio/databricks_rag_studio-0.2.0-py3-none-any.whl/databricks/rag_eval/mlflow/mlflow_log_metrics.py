"""Generate the metrics logged into MLflow."""

import collections
from typing import List, Dict, Optional, Mapping

import numpy as np

from databricks.rag_eval.evaluation import entities, schemas


_AVERAGE_SUFFIX = "/average"


def generate_mlflow_metrics(
    eval_results: List[entities.EvalResult],
) -> Dict[str, float]:
    """
    Generates per-run MLflow metrics.

    :param eval_results: List of EvalResult objects
    :return: Dictionary of aggregated MLflow metrics
    """

    result = {
        **{
            f"{schemas.GROUND_TRUTH_RETRIEVAL_METRIC_COL_PREFIX}{metric_name}{_AVERAGE_SUFFIX}": metric_value
            for metric_name, metric_value in _compute_avg_for_metric_group(
                eval_results, "ground_truth_retrieval_metrics"
            ).items()
        },
        **{
            f"{schemas.LLM_JUDGED_RETRIEVAL_METRIC_COL_PREFIX}{metric_name}{_AVERAGE_SUFFIX}": metric_value
            for metric_name, metric_value in _compute_avg_for_metric_group(
                eval_results, "llm_judged_retrieval_metrics"
            ).items()
        },
        **{
            f"{schemas.LLM_JUDGED_RESPONSE_METRIC_COL_PREFIX}{assessment_name}_rating{_AVERAGE_SUFFIX}": true_rate
            for assessment_name, true_rate in _compute_true_rate_answer_assessment(
                eval_results
            ).items()
        },
    }

    # Other generation avg metrics
    for metric_name in [
        "request_token_count",
        "response_token_count",
        "total_input_token_count",
        "total_output_token_count",
        "total_token_count",
        "latency_seconds",
    ]:
        metric_value = _compute_avg_for_metric(eval_results, metric_name)
        if metric_value is not None:
            result[f"chain/{metric_name}{_AVERAGE_SUFFIX}"] = metric_value

    return result


def _compute_avg_for_metric_group(
    eval_results: List[entities.EvalResult],
    metric_group_name: str,
) -> Dict[str, float]:
    """
    Compute the average a group of metrics across all eval results.
    The metric group is expected to be a Mapping[str, float] in each EvalResult.

    :param eval_results: List of EvalResult objects
    :param metric_group_name: Name of the metric group
    :return: Dictionary of average value for each metric in the group
    """
    metric_value_sums = collections.defaultdict(float)
    metric_value_counts = collections.defaultdict(int)
    for eval_result in eval_results:
        metric_group: Mapping[str, float] = getattr(eval_result, metric_group_name, {})
        for (
            metric_name,
            metric_value,
        ) in metric_group.items():
            metric_value_sums[metric_name] += metric_value
            metric_value_counts[metric_name] += 1
    return {
        metric_name: metric_value_sums[metric_name] / metric_value_counts[metric_name]
        for metric_name in metric_value_sums
        if metric_value_counts[metric_name] > 0
    }


def _compute_avg_for_metric(
    eval_results: List[entities.EvalResult], metric_name: str
) -> Optional[float]:
    """
    Compute the average of a metric across all eval results.

    Returns None if the metric is not present in any of the eval results.

    :param eval_results: List of EvalResult objects
    :param metric_name: Name of the metric
    :return: Average of the metric
    """
    metric_values = [
        getattr(eval_result, metric_name, None)
        for eval_result in eval_results
        if getattr(eval_result, metric_name, None) is not None
    ]

    return np.average(metric_values) if metric_values else None


def _count_true_for_metric(
    eval_results: List[entities.EvalResult], metric_name: str
) -> int:
    """
    Count the number of `True` of a metric across all eval results.

    :param eval_results: List of EvalResult objects
    :param metric_name: Name of the metric
    :return: Count of the metric
    """
    return np.count_nonzero(
        [getattr(eval_result, metric_name, None) for eval_result in eval_results]
    )


def _compute_true_rate_answer_assessment(
    eval_results: List[entities.EvalResult],
) -> Dict[str, float]:
    """
    Compute the rate of `True` in the answer assessment results.

    rate of `True` = count of `True` / count of non-null values.

    :param eval_results: List of EvalResult objects
    :return: Dictionary of rate of `True` for each answer assessment
    """
    true_counts = collections.defaultdict(int)
    non_null_counts = collections.defaultdict(int)
    for eval_result in eval_results:
        for assessment_result in eval_result.assessment_results:
            if isinstance(assessment_result, entities.AnswerAssessmentResult):
                true_counts[assessment_result.assessment_name] += (
                    assessment_result.rating.bool_value is True
                )
                non_null_counts[assessment_result.assessment_name] += (
                    assessment_result.rating.bool_value is not None
                )

    return {
        assessment_name: (
            (true_counts[assessment_name] / non_null_counts[assessment_name])
            if non_null_counts[assessment_name] > 0
            else 0.0
        )
        for assessment_name in true_counts
    }
