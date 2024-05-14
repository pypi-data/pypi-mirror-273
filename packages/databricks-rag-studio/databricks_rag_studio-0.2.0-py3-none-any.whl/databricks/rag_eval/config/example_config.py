import dataclasses
from typing import Mapping, Any, Optional

from databricks.rag_eval.utils.collection_utils import omit_keys


@dataclasses.dataclass(frozen=True)
class AssessmentExample:
    """
    User-provided example to guide the LLM judge in deciding on the True/False value
    for a particular assessment.
    ex. User provided example yaml:
    ```
    - context: some context
      response: some response
      value: True
      rationale: some rationale

    will be parsed into the following AssessmentExample object:
    ```
    AssessmentExample(
        variables={"context": "some context", "response": "some response"},
        value=True,
        rationale="some rationale"
    )
    ```
    """

    variables: dict[str, str]
    """
    Mapping from variable name to variable value. Should be validated against corresponding
    assessment config to ensure all required columns are present.
    """

    value: str
    """
    Whether the output should be considered satisfactory or unsatisfactory for the assessment.
    """
    rationale: Optional[str] = None
    """
    Explanation of why the output was given its value.
    """

    @classmethod
    def from_dict(cls, example_dict: Mapping[str, Any]):
        VALUE = "value"
        RATIONALE = "rationale"

        value = str(example_dict[VALUE]).strip()
        if value.lower() not in ["true", "false"]:
            raise ValueError(
                f"Invalid value for example: {value}. Must be either 'True' or 'False'."
            )

        return cls(
            variables=omit_keys(example_dict, [VALUE, RATIONALE]),
            value=value,
            rationale=example_dict.get(RATIONALE),
        )
