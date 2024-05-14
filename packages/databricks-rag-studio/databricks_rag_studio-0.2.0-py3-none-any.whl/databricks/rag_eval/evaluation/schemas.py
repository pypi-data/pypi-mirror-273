from typing import Union, List, TypeVar


######################################################################
# Column/field names used in MLflow EvaluationDataset DataFrames
######################################################################
DOC_URI_COL = "doc_uri"
CHUNK_CONTENT_COL = "content"
TRACE_COL = "trace"
REQUEST_ID_COL = "request_id"
REQUEST_COL = "request"
EXPECTED_RETRIEVED_CONTEXT_COL = "expected_retrieved_context"
EXPECTED_RESPONSE_COL = "expected_response"
RESPONSE_COL = "response"
RETRIEVED_CONTEXT_COL = "retrieved_context"

######################################################################
# Column/field names for the output pandas DataFrame of mlflow.evaluate
######################################################################
_CHAIN_PREFIX = "chain/"
TOTAL_INPUT_TOKEN_COUNT_COL = _CHAIN_PREFIX + "total_input_token_count"
TOTAL_OUTPUT_TOKEN_COUNT_COL = _CHAIN_PREFIX + "total_output_token_count"
TOTAL_TOKEN_COUNT_COL = _CHAIN_PREFIX + "total_token_count"
LATENCY_SECONDS_COL = _CHAIN_PREFIX + "latency_seconds"
REQUEST_TOKEN_COUNT = _CHAIN_PREFIX + "request_token_count"
RESPONSE_TOKEN_COUNT = _CHAIN_PREFIX + "response_token_count"

_RETRIEVAL_PREFIX = "retrieval/"
GROUND_TRUTH_RETRIEVAL_METRIC_COL_PREFIX = _RETRIEVAL_PREFIX + "ground_truth/"
GROUND_TRUTH_DOCUMENT_PREFIX = "document_"
LLM_JUDGED_RETRIEVAL_METRIC_COL_PREFIX = _RETRIEVAL_PREFIX + "llm_judged/"

_RESPONSE_PREFIX = "response/"
LLM_JUDGED_RESPONSE_METRIC_COL_PREFIX = _RESPONSE_PREFIX + "llm_judged/"

######################################################################
# Data types for the output pandas DataFrame of mlflow.evaluate
######################################################################
ASSESSMENT_RESULT_TYPE: TypeVar = TypeVar(
    "ASSESSMENT_RESULT_TYPE", bool, str, None, List[Union[bool, str, None]]
)
METRIC_RESULT_TYPE: TypeVar = TypeVar("METRIC_RESULT_TYPE", float, int, None)
