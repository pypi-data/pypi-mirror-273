"""
This module contains helper functions for invoking the model to be evaluated.
"""

import logging
from dataclasses import dataclass
from typing import Dict, Optional, List, Tuple, NewType

import mlflow
import mlflow.entities as mlflow_entities
import mlflow.pyfunc.context as pyfunc_context

from databricks.rag_eval.evaluation import entities, traces

_MODEL_INPUT__MESSAGES_COL = "messages"
_MODEL_INPUT__ROLE_COL = "role"
_MODEL_INPUT__CONTENT_COL = "content"
_MODEL_INPUT__USER_ROLE = "user"


ModelOutput = NewType("ModelOutput", List[str])


_logger = logging.getLogger(__name__)


@dataclass
class ModelResult:
    """
    The result of invoking the model.
    """

    response: Optional[str]
    retrieval_context: Optional[entities.RetrievalContext]
    trace: Optional[mlflow_entities.Trace]
    error_message: Optional[str]

    @classmethod
    def from_outputs(
        cls,
        *,
        response: Optional[str],
        retrieval_context: Optional[entities.RetrievalContext],
        trace: Optional[mlflow_entities.Trace],
    ) -> "ModelResult":
        """Build a normal model result with response and retrieval context."""
        return cls(
            response=response,
            retrieval_context=retrieval_context,
            trace=trace,
            error_message=None,
        )

    @classmethod
    def from_error_message(cls, error_message: str) -> "ModelResult":
        """Build a model result with an error message."""
        return cls(
            response=None,
            retrieval_context=None,
            trace=None,
            error_message=error_message,
        )


def invoke_model(
    model: mlflow.pyfunc.PyFuncModel, eval_item: entities.EvalItem
) -> ModelResult:
    """
    Invoke the model with a request to get a model result.

    :param model: The model to invoke.
    :param eval_item: The eval item containing the request.
    :return: The model result.
    """
    try:
        # Convert the request string to the model input format
        model_input = _to_model_input_format(eval_item.question)
        # Invoke the model
        model_output, trace = _model_predict_with_trace(
            model, model_input, eval_item.question_id
        )
        # Get the response from the model output
        response = _get_response_from_predictions(model_output)
        retrieval_context = traces.extract_retrieval_context_from_trace(trace)

        model_result = ModelResult.from_outputs(
            response=response,
            retrieval_context=retrieval_context,
            trace=trace,
        )
        return model_result

    except Exception as e:
        model_result = ModelResult.from_error_message(
            f"Fail to invoke the model: {e!r}"
        )
        return model_result


def _to_model_input_format(request: str) -> Dict:
    """
    Convert the request string to the format expected by the model.

    :param request: The request string
    :return: The model input format
    """
    return {
        _MODEL_INPUT__MESSAGES_COL: [
            {
                _MODEL_INPUT__ROLE_COL: _MODEL_INPUT__USER_ROLE,
                _MODEL_INPUT__CONTENT_COL: request,
            },
        ]
    }


def _model_predict_with_trace(
    model: mlflow.pyfunc.PyFuncModel, model_input: Dict, request_id: str
) -> Tuple[ModelOutput, mlflow_entities.Trace]:
    """
    Invoke the model to get output and trace.

    :param model: The langchain model
    :param model_input: The model input
    :param request_id: The request id
    :return: The response and the retrieval context
    """
    try:
        with pyfunc_context.set_prediction_context(
            pyfunc_context.Context(request_id, is_evaluate=True)
        ):
            model_output = model.predict(model_input)
            trace = mlflow.get_trace(request_id)
        return model_output, trace
    except Exception as e:
        raise ValueError(f"Fail to invoke the model with {model_input}. {e!r}")


def _get_response_from_predictions(model_output: ModelOutput) -> Optional[str]:
    """
    Get the response string from the model output.

    Model output could be:
     - a string, which is the response; or
     - a list of string, in which the first string is the response; or
     - a LLMResult to_dict() output, e.g. { 'generations': [ [ { 'text': 'xxx', ... } ] ], ... }; or
     - other complex types, which are directly converted to string with str().

     If fails to parse the model output, return None.

    :param model_output: The model output object
    :return: The response string
    """
    try:
        if model_output is None:
            return None
        elif isinstance(model_output, str):
            return model_output
        elif isinstance(model_output, list):
            return model_output[0] if len(model_output) > 0 else None
        elif isinstance(model_output, dict) and "generations" in model_output:
            return model_output["generations"][0][0]["text"]
        else:
            return str(model_output)
    except Exception as e:
        _logger.debug(f"Fail to parse the model output: {model_output}. {e!r}")
        return None
