import dataclasses
import numbers
from dataclasses import field
from typing import Dict, Any, Optional, Mapping, List

from databricks.rag_eval.utils import enum_utils, rate_limit, prompt_utils
from databricks.rag_eval.config import constants as config_constants, example_config

_ALLOWED_VARIABLES = [
    config_constants.ALLOWED_PROMPT_VARIABLE__REQUEST,
    config_constants.ALLOWED_PROMPT_VARIABLE__RESPONSE,
    config_constants.ALLOWED_PROMPT_VARIABLE__CONTEXT,
    config_constants.ALLOWED_PROMPT_VARIABLE__EXPECTED_RESPONSE,
]


@dataclasses.dataclass(frozen=True)
class RateLimitConfig:
    """
    Rate limit configuration for the RAG evaluation harness.
    """

    quota: float
    """
    The number of tasks allowed to run in the time window.
    """

    time_window_in_seconds: float
    """
    The time window in seconds.
    """


@dataclasses.dataclass(frozen=True)
class AssessmentSource:
    """
    Represents the source of the assessment.

    A source uniquely identifies an assessment judge. Each source has its own rate limiter.
    """

    source_id: str
    """The ID of the source."""

    model: str
    """The model to use for the LLM judge. For example, "endpoints:/databricks-llama-2-70b-chat"."""

    rate_limiter: rate_limit.RateLimiter
    """
    Client-side rate limiter for the LLM judge.
    Using NoOpRateLimiter means no client-side rate limiting is applied.
    """


@dataclasses.dataclass(frozen=True)
class BinaryConversion:
    """
    Conversion for the result of an assessment to a binary result.
    """

    threshold: float
    """
    Threshold value for converting to the binary.
    If not None, it means the output of the metric can be converted to a binary result
    and set as the bool_value in the ratings.
    """
    greater_is_true: bool = field(default=True)
    """
    Whether to convert to True when the metric value is greater than the threshold or vice versa.
    If True, the bool_value is True when the metric value score is greater than or equal to the threshold.
    If False, the bool_value is True when the metric value score is less than or equal to the threshold.
    """

    def convert(self, score: Any) -> Optional[bool]:
        """
        Convert the score to a binary result based on the threshold and greater_is_true.

        If the score is not a real number, return None.
        """
        if isinstance(score, numbers.Real):
            # noinspection PyTypeChecker
            return (
                score >= self.threshold
                if self.greater_is_true
                else score <= self.threshold
            )
        else:
            return None

    def convert_to_score(self, value: str) -> str:
        """
        Convert the binary result back to a score based on the threshold and greater_is_true.
        """
        return "5" if self.greater_is_true == (value.lower() == "true") else "1"


class AssessmentType(enum_utils.StrEnum):
    """Type of the assessment."""

    RETRIEVAL = "RETRIEVAL"
    """Assessment for retrieval. This is used to assess the quality of retrieval."""
    ANSWER = "ANSWER"
    """Assessment for answer. This is used to assess the quality of answer."""


@dataclasses.dataclass(frozen=True)
class AssessmentConfig:
    assessment_name: str

    assessment_type: AssessmentType

    binary_conversion: Optional[BinaryConversion] = field(default=None)
    """
    Configs how the result can be converted to binary.
    None if the result is not for converting to binary.
    """
    # TODO(ML-40164): clean these bools into an array of required columns
    require_question: bool = field(default=False)
    """Whether the assessment requires input to be present in the dataset to eval."""

    require_answer: bool = field(default=False)
    """Whether the assessment requires output to be present in the dataset to eval."""

    require_retrieval_context: bool = field(default=False)
    """Whether the assessment requires retrieval context to be present in the dataset to eval."""

    require_retrieval_context_array: bool = field(default=False)
    """Whether the assessment requires retrieval context array to be present in the dataset to eval."""

    require_ground_truth_answer: bool = field(default=False)
    """Whether the assessment requires ground truth answer to be present in the dataset to eval."""

    require_ground_truth_retrieval_context: bool = field(default=False)
    """Whether the assessment requires ground truth retrieval to be present in the dataset to eval."""


@dataclasses.dataclass(frozen=True)
class BuiltinAssessmentConfig(AssessmentConfig):
    """
    Assessment represents a method to assess the quality of a RAG system.

    The method is defined by an MLflow EvaluationMetric object.
    """

    module_path: str = dataclasses.field(default="")
    """
    Module path of the function to create the MLflow EvaluationMetric object.
    For example, "mlflow.metrics.genai.relevance".
    """

    args: Dict[str, Any] = field(default_factory=dict)
    """
    Special arguments supplied when calling the function to create the MLflow EvaluationMetric object.
    This takes precedence over the common arguments such as `model` and `examples`
    """

    def __hash__(self):
        """
        Allow this object to be used as a key in a dictionary.
        """
        return hash(self.assessment_name)


@dataclasses.dataclass(frozen=True)
class CustomAssessmentConfig(AssessmentConfig):
    """
    Represents user-provided config values for a custom assessment.

    This method is defined by an MLflow EvaluationMetric object, produced
    by internally calling `make_custom_genai_metric`.
    """

    prompt_template: str = dataclasses.field(default="")

    @classmethod
    def from_dict(cls, assessment_dict: Mapping[str, Any]) -> "CustomAssessmentConfig":
        """
        Create a CustomAssessmentConfig object from a dictionary.
        Input dict should have the following form:
        {
            "name": "assessment_name",
            "type": "RETRIEVAL" or "ANSWER",
            "definition": "prompt_template"
        }
        """
        ASSESSMENT_NAME = "name"
        ASSESSMENT_TYPE = "type"
        PROMPT_TEMPLATE = "definition"
        # Parse required columns from the prompt.
        name = assessment_dict[ASSESSMENT_NAME]
        prompt_template = assessment_dict[PROMPT_TEMPLATE]
        assessment_type = AssessmentType(assessment_dict[ASSESSMENT_TYPE])

        variable_names = prompt_utils.get_variables_from_template(prompt_template)
        if any(var not in _ALLOWED_VARIABLES for var in variable_names):
            raise ValueError(
                f"Invalid variable in prompt: {variable_names}. Allowed variables: {', '.join(_ALLOWED_VARIABLES)}"
            )

        return cls(
            assessment_name=name,
            assessment_type=assessment_type,
            require_question=config_constants.ALLOWED_PROMPT_VARIABLE__REQUEST
            in variable_names,
            require_answer=config_constants.ALLOWED_PROMPT_VARIABLE__RESPONSE
            in variable_names,
            require_retrieval_context=config_constants.ALLOWED_PROMPT_VARIABLE__CONTEXT
            in variable_names
            and assessment_type == AssessmentType.ANSWER,
            require_retrieval_context_array=config_constants.ALLOWED_PROMPT_VARIABLE__CONTEXT
            in variable_names
            and assessment_type == AssessmentType.RETRIEVAL,
            require_ground_truth_answer=config_constants.ALLOWED_PROMPT_VARIABLE__EXPECTED_RESPONSE
            in variable_names,
            require_ground_truth_retrieval_context=False,  # Don't support this for custom assessments. This will be removed.
            # True/false by default
            binary_conversion=BinaryConversion(threshold=5),
            prompt_template=prompt_template,
        )

    def __hash__(self):
        """
        Allow this object to be used as a key in a dictionary.
        """
        return hash(self.assessment_name)


def validate_example_has_required_fields(
    assessment_conf: AssessmentConfig, examples: List[example_config.AssessmentExample]
):
    """
    Validate that the example has all the required fields for the assessment. Allows extraneous variables in examples.
    """
    required_fields = []
    if assessment_conf.require_question:
        required_fields.append(config_constants.ALLOWED_PROMPT_VARIABLE__REQUEST)
    if assessment_conf.require_answer:
        required_fields.append(config_constants.ALLOWED_PROMPT_VARIABLE__RESPONSE)
    if (
        assessment_conf.require_retrieval_context
        or assessment_conf.require_retrieval_context_array
    ):
        required_fields.append(config_constants.ALLOWED_PROMPT_VARIABLE__CONTEXT)
    if assessment_conf.require_ground_truth_answer:
        required_fields.append(
            config_constants.ALLOWED_PROMPT_VARIABLE__EXPECTED_RESPONSE
        )

    if any(
        [
            field not in example.variables
            for field in required_fields
            for example in examples
        ]
    ):
        raise ValueError(
            f"Missing at least one required field in examples for assessment {assessment_conf.assessment_name}: {', '.join(required_fields)}"
        )
