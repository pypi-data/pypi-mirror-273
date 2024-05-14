"""Methods and classes for working with configuration files."""

import dataclasses
import io
from typing import List, Mapping, Any

import yaml

from databricks.rag_eval.config import judge_config
from databricks.rag_eval.utils.collection_utils import omit_keys

BUILTIN_ASSESSMENTS_KEY = "builtin_assessments"
ASSESSMENT_JUDGES_KEY = "assessment_judges"


def _get_yaml_dump_or_empty_string(config_dict: Mapping[str, Any], key: str) -> str:
    """Returns a YAML dump of the specified key's value from the config dict if present and not empty, otherwise an empty string."""
    value = config_dict.get(key)
    if value:
        return yaml.safe_dump(value, default_flow_style=False, sort_keys=False)
    return ""


@dataclasses.dataclass
class EvaluationConfig:
    """Abstraction for `evaluation` config"""

    assessment_judges: List[judge_config.AssessmentJudge] = dataclasses.field(
        default_factory=list
    )
    _builtin_assessments_str: str = ""
    _custom_assessment_judges_str: str = ""

    def __post_init__(self):
        if self.assessment_judges is None:
            self.assessment_judges = []

    @classmethod
    def from_dict(cls, config_dict: Mapping[str, Any]):
        if (
            ASSESSMENT_JUDGES_KEY not in config_dict
            and BUILTIN_ASSESSMENTS_KEY not in config_dict
        ):
            raise ValueError(
                f"Invalid config {config_dict}: at least one of `{ASSESSMENT_JUDGES_KEY}` or `{BUILTIN_ASSESSMENTS_KEY}` required."
            )

        try:
            builtin_assessment_judges = judge_config.create_builtin_judges(
                config_dict.get(BUILTIN_ASSESSMENTS_KEY) or []
            )
        except (TypeError, KeyError, ValueError) as error:
            raise ValueError(
                f"Invalid config `{config_dict[BUILTIN_ASSESSMENTS_KEY]}`: {error}"
            )
        try:
            custom_assessment_judges = [
                judge_config.create_custom_judge(judge)
                for judge in config_dict.get(ASSESSMENT_JUDGES_KEY) or []
            ]
        except (TypeError, KeyError, ValueError) as error:
            raise ValueError(
                f"Invalid config `{config_dict[ASSESSMENT_JUDGES_KEY]}`: {error}"
            )
        assessment_judges = builtin_assessment_judges + custom_assessment_judges
        all_names = [
            assessment_conf.assessment_name
            for judge in assessment_judges
            for assessment_conf in judge.assessment_configs_and_examples.keys()
        ]
        dups = {name for name in all_names if all_names.count(name) > 1}
        if dups:
            raise ValueError(
                f"Invalid config `{config_dict}`: assessment names must be unique. Found duplicate assessment names: {dups}"
            )

        builtin_assessments_str = _get_yaml_dump_or_empty_string(
            config_dict, BUILTIN_ASSESSMENTS_KEY
        )
        assessment_judges_str = _get_yaml_dump_or_empty_string(
            config_dict, ASSESSMENT_JUDGES_KEY
        )

        try:
            result = cls(
                assessment_judges=assessment_judges,
                _builtin_assessments_str=builtin_assessments_str,
                _custom_assessment_judges_str=assessment_judges_str,
                **omit_keys(
                    config_dict, [ASSESSMENT_JUDGES_KEY, BUILTIN_ASSESSMENTS_KEY]
                ),
            )
        except (TypeError, KeyError, ValueError) as error:
            raise ValueError(f"Invalid config `{config_dict}`: {error}")

        return result

    @classmethod
    def from_file(cls, file_path: str) -> "EvaluationConfig":
        """Reads the config from a file"""
        with open(file_path, "r") as file:
            config_dict = yaml.safe_load(file)
        return cls.from_dict(config_dict)

    @classmethod
    def from_yaml(cls, yaml_config: str) -> "EvaluationConfig":
        """Reads the config from a YAML string"""
        yaml_stream = io.StringIO(yaml_config)
        try:
            config_dict = yaml.safe_load(yaml_stream)
        except Exception as error:
            raise ValueError(f"Error reading config from YAML: {error}")

        return cls.from_dict(config_dict)

    def get_builtin_assessments_str(self) -> str:
        """Returns the string representation of the builtin assessments"""
        return self._builtin_assessments_str

    def get_custom_assessment_judges_str(self) -> str:
        """Returns the string representation of the custom assessment judges"""
        return self._custom_assessment_judges_str


def default_config() -> str:
    """Returns the default config (in YAML)"""
    # TODO[ML-40686]: add back harmfulness to default when Llama-guard integration is completed
    return """
builtin_assessments:
  - groundedness
  - correctness
  - relevance_to_query
  - chunk_relevance
"""
