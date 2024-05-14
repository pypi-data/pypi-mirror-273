from typing import List

from databricks.rag_eval.config.assessment_config import (
    AssessmentType,
    BinaryConversion,
    BuiltinAssessmentConfig,
)
from databricks.rag_eval import constants

DEFAULT_BINARY_CONVERSION_FOR_LLM_JUDGE = BinaryConversion(
    threshold=constants.DEFAULT_THRESHOLD_FOR_LLM_JUDGE
)

# ================ Answer Assessments ================
GROUNDEDNESS = BuiltinAssessmentConfig(
    assessment_name="groundedness",
    assessment_type=AssessmentType.ANSWER,
    module_path="mlflow.metrics.genai.faithfulness",
    require_question=True,
    require_answer=True,
    require_retrieval_context=True,
    binary_conversion=DEFAULT_BINARY_CONVERSION_FOR_LLM_JUDGE,
)

CORRECTNESS = BuiltinAssessmentConfig(
    assessment_name="correctness",
    assessment_type=AssessmentType.ANSWER,
    module_path="mlflow.metrics.genai.answer_correctness",
    require_question=True,
    require_answer=True,
    require_ground_truth_answer=True,
    binary_conversion=DEFAULT_BINARY_CONVERSION_FOR_LLM_JUDGE,
)

HARMFULNESS = BuiltinAssessmentConfig(
    assessment_name="harmfulness",
    assessment_type=AssessmentType.ANSWER,
    # TODO[ML-40686]: Temporarily make harmful assessment a no-op; the actual implementation will be on the service side
    module_path="databricks.rag_eval.evaluation.metrics.no_op",
    require_question=True,
    require_answer=True,
)

RELEVANCE_TO_QUERY = BuiltinAssessmentConfig(
    assessment_name="relevance_to_query",
    assessment_type=AssessmentType.ANSWER,
    module_path="mlflow.metrics.genai.answer_relevance",
    require_question=True,
    require_answer=True,
    binary_conversion=DEFAULT_BINARY_CONVERSION_FOR_LLM_JUDGE,
)

# ================ Retrieval Assessments ================
CHUNK_RELEVANCE = BuiltinAssessmentConfig(
    assessment_name="chunk_relevance",
    assessment_type=AssessmentType.RETRIEVAL,
    module_path="databricks.rag_eval.judges.content_relevance",
    require_question=True,
    require_retrieval_context_array=True,
    binary_conversion=DEFAULT_BINARY_CONVERSION_FOR_LLM_JUDGE,
)


def builtin_assessment_configs() -> List[BuiltinAssessmentConfig]:
    """Returns the list of built-in assessment configs"""
    return [
        HARMFULNESS,
        GROUNDEDNESS,
        CORRECTNESS,
        RELEVANCE_TO_QUERY,
        CHUNK_RELEVANCE,
    ]


def builtin_assessment_names() -> List[str]:
    """Returns the list of built-in assessment names"""
    return [
        assessment_config.assessment_name
        for assessment_config in builtin_assessment_configs()
    ]


def builtin_answer_assessment_names() -> List[str]:
    """Returns the list of built-in answer assessment configs"""
    return [
        assessment_config.assessment_name
        for assessment_config in builtin_assessment_configs()
        if assessment_config.assessment_type == AssessmentType.ANSWER
    ]


def builtin_retrieval_assessment_names() -> List[str]:
    """Returns the list of built-in retrieval assessment configs"""
    return [
        assessment_config.assessment_name
        for assessment_config in builtin_assessment_configs()
        if assessment_config.assessment_type == AssessmentType.RETRIEVAL
    ]


def get_builtin_assessment_config_with_name(
    name: str,
) -> BuiltinAssessmentConfig:
    """Returns the built-in assessment config with the given name"""
    for assessment_config in builtin_assessment_configs():
        if assessment_config.assessment_name == name:
            return assessment_config
    raise ValueError(
        f"Assessment '{name}' not found in the builtin assessments. "
        f"Available assessments: {builtin_assessment_names()}."
    )
