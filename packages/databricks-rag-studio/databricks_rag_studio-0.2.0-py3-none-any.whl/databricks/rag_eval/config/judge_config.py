import dataclasses
from typing import Mapping, Any, Tuple, List, Dict, Union

from databricks.rag_eval import constants
from databricks.rag_eval.config import assessment_config, example_config
from databricks.rag_eval.judges import builtin_judge


def _get_key_value_from_single_key_dict(d: Mapping[str, Any]) -> Tuple[str, Any]:
    if len(d) != 1:
        raise ValueError(f"Expected single-key dict, got {d}")
    return next(iter(d.items()))


@dataclasses.dataclass(frozen=True)
class AssessmentJudge:
    """Abstraction for an entry in `assessment_judges` section in the config file"""

    judge_name: str
    endpoint_name: str
    # TODO(ML-40455): Move examples directly into AssessmentConfig once builtins are moved
    # to service
    assessment_configs_and_examples: Dict[
        assessment_config.AssessmentConfig, List[example_config.AssessmentExample]
    ] = dataclasses.field(default_factory=dict)


def _parse_builtin_examples(
    assessment_list: List[Union[str, Dict[str, Any]]]
) -> Dict[
    assessment_config.BuiltinAssessmentConfig, List[example_config.AssessmentExample]
]:
    """
    Parse a list of builtin assessments (and optional examples) into a map from BuiltinAssessmentConfig to
    list of AssessmentExample.
    """
    # Assessments is a list of either assessment names, or single-key dicts mapping assessment names
    # to list of examples. Want to turn this into a single dict mapping assessment names to lists of
    # examples.
    assessment_configs = {}

    for assessment in assessment_list:
        if isinstance(assessment, dict):
            # Single-key dict from assessment name to examples. ex.
            # { 'correctness': { 'examples': [ ... ] } }
            assessment_name, assessment_conf = _get_key_value_from_single_key_dict(
                assessment
            )
        elif isinstance(assessment, str):
            # Just the assessment name. ex. 'correctness'
            assessment_name, assessment_conf = assessment, {}
        else:
            raise ValueError(
                f"Invalid config: expected string or dict, got {assessment}"
            )

        assessment_examples = [
            example_config.AssessmentExample.from_dict(example)
            for example in assessment_conf.get("examples", [])
        ]
        builtin_assessment_conf = builtin_judge.get_builtin_assessment_config_with_name(
            assessment_name
        )
        assessment_configs[builtin_assessment_conf] = assessment_examples

    return assessment_configs


def create_custom_judge(judge_dict: Mapping[str, Any]):
    ASSESSMENTS_KEY = "assessments"
    JUDGE_NAME_KEY = "judge_name"
    ENDPOINT_NAME_KEY = "endpoint_name"

    judge_name = judge_dict[JUDGE_NAME_KEY]
    endpoint_name = judge_dict.get(ENDPOINT_NAME_KEY)
    # if this is for a built-in databricks judge, then the endpoint will be automatically set
    # TODO(ML-40164): Use a better flag to model builtin judges
    if judge_name == constants.DATABRICKS_JUDGE_NAME:
        raise ValueError("Cannot re-configure built-in assessment judge.")

    if endpoint_name is None:
        raise ValueError(f"Endpoint must be set for custom judge: {judge_name}")

    if not endpoint_name.strip().startswith(constants.ALLOWED_CUSTOM_ENDPOINTS_PREFIX):
        raise ValueError(
            f"Invalid endpoint name: {endpoint_name}. Endpoint must be an external model."
        )

    assessment_list = judge_dict.get(ASSESSMENTS_KEY, []) or []
    if judge_name == constants.DATABRICKS_JUDGE_NAME:
        assessment_configs_and_examples = _parse_builtin_examples(assessment_list)
    else:
        assessment_configs_and_examples = {
            assessment_config.CustomAssessmentConfig.from_dict(assessment_dict): [
                example_config.AssessmentExample.from_dict(example)
                for example in assessment_dict.get("examples", [])
            ]
            for assessment_dict in assessment_list
        }
        invalid_names = [
            assessment_conf.assessment_name
            for assessment_conf in assessment_configs_and_examples.keys()
            if assessment_conf.assessment_name
            in builtin_judge.builtin_assessment_names()
        ]
        if invalid_names:
            raise ValueError(
                f"Invalid config: custom assessment judge cannot use built-in assessment names: {', '.join(invalid_names)}"
            )
        for assessment_conf, examples in assessment_configs_and_examples.items():
            assessment_config.validate_example_has_required_fields(
                assessment_conf, examples
            )

    return AssessmentJudge(
        judge_name=judge_name,
        endpoint_name=endpoint_name,
        assessment_configs_and_examples=assessment_configs_and_examples,
    )


def create_builtin_judges(
    assessment_list: List[Union[str, Dict[str, Any]]]
) -> List[AssessmentJudge]:
    """
    Create AssessmentJudge objects from a list of builtin assessments and optional examples.
    This judge can only use the predefined builtin assessments names and model endpoint.
    """
    builtin_assessment_config_to_examples = _parse_builtin_examples(assessment_list)
    for assessment_conf, examples in builtin_assessment_config_to_examples.items():
        assessment_config.validate_example_has_required_fields(
            assessment_conf, examples
        )

    return (
        [
            AssessmentJudge(
                judge_name=constants.DATABRICKS_JUDGE_NAME,
                endpoint_name=constants.DATABRICKS_JUDGE_DEFAULT_ENDPOINT,
                assessment_configs_and_examples=builtin_assessment_config_to_examples,
            )
        ]
        if builtin_assessment_config_to_examples
        else []
    )
