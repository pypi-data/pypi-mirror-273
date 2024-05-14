"""This module deals with trace and extracting information from traces."""

import dataclasses
import logging
from typing import Optional, List

import mlflow.entities as mlflow_entities
import mlflow.tracing.constant as mlflow_tracing_constant

from databricks.rag_eval.evaluation import entities
from databricks.rag_eval.utils import token_count_utils

_logger = logging.getLogger(__name__)


def _span_is_type(
    span: mlflow_entities.Span,
    span_type: str | List[str],
) -> bool:
    """Check if the span is of a certain span type or one of the span types in the collection"""
    if span.attributes is None:
        return False
    if not isinstance(span_type, List):
        span_type = [span_type]
    return (
        span.attributes.get(mlflow_tracing_constant.SpanAttributeKey.SPAN_TYPE)
        in span_type
    )


# ================== Retrieval Context ==================
def extract_retrieval_context_from_trace(
    trace: Optional[mlflow_entities.Trace],
) -> Optional[entities.RetrievalContext]:
    """
    Extract the retrieval context from the trace.

    Only consider the last retrieval span in the trace if there are multiple retrieval spans.

    If the trace does not have a retrieval span, return None.

    :param trace: The trace
    :return: The retrieval context
    """
    if trace is None or trace.data is None:
        return None

    retrieval_spans = [
        span
        for span in trace.data.spans or []
        if _span_is_type(span, mlflow_entities.SpanType.RETRIEVER)
    ]
    if len(retrieval_spans) == 0:
        return None
    # Only consider the last retrieval span
    retrieval_span = retrieval_spans[-1]
    return _extract_retrieval_context_from_retrieval_span(retrieval_span)


def _extract_retrieval_context_from_retrieval_span(
    span: mlflow_entities.Span,
) -> Optional[entities.RetrievalContext]:
    """Get the retrieval context from a retrieval span."""
    try:
        retriever_outputs = span.attributes.get(
            mlflow_tracing_constant.SpanAttributeKey.OUTPUTS
        )
        return entities.RetrievalContext(
            [
                (
                    entities.Chunk(
                        doc_uri=(
                            chunk.get("metadata", {}).get("doc_uri") if chunk else None
                        ),
                        content=chunk.get("page_content") if chunk else None,
                    )
                )
                for chunk in retriever_outputs or []
            ]
        )
    except Exception as e:
        _logger.debug(f"Fail to get retrieval context from span: {span}. Error: {e!r}")
        return None


# ================== Token Count ==================
@dataclasses.dataclass
class TraceTokenCount:
    input_token_count: Optional[int] = None
    output_token_count: Optional[int] = None

    @property
    def total_token_count(self) -> Optional[int]:
        if self.input_token_count is not None and self.output_token_count is not None:
            return self.input_token_count + self.output_token_count
        return None


def compute_total_token_count(
    trace: Optional[mlflow_entities.Trace],
) -> TraceTokenCount:
    """
    Compute the total input/output tokens across all trace spans.

    :param trace: The trace object

    :return: Total input/output token counts
    """
    if trace is None or trace.data is None:
        return TraceTokenCount()

    # Only consider leaf spans that is of type LLM or CHAT_MODEL.
    # Depending on the implementation of LLM/CHAT_MODEL components,
    # a span may have multiple children spans that are also LLM/CHAT_MODEL spans.
    # But only the leaf spans send requests to the LLM.
    # To avoid double counting, we only consider leaf spans.
    leaf_spans = _get_leaf_spans(trace)
    leaf_llm_or_chat_model_spans = [
        span
        for span in leaf_spans
        if _span_is_type(
            span, [mlflow_entities.SpanType.LLM, mlflow_entities.SpanType.CHAT_MODEL]
        )
    ]

    input_token_counts = []
    output_token_counts = []
    for span in leaf_llm_or_chat_model_spans:
        # Input
        input_text = _extract_input_text_from_span(span)
        input_token_count = token_count_utils.compute_token_count(input_text)
        if input_token_count is not None:
            input_token_counts.append(input_token_count)
        # Output
        output_text = _extract_output_text_from_span(span)
        output_token_count = token_count_utils.compute_token_count(output_text)
        if output_token_count is not None:
            output_token_counts.append(output_token_count)
    return TraceTokenCount(
        input_token_count=(
            sum(input_token_counts) if len(input_token_counts) > 0 else None
        ),
        output_token_count=(
            sum(output_token_counts) if len(output_token_counts) > 0 else None
        ),
    )


def _get_leaf_spans(trace: mlflow_entities.Trace) -> List[mlflow_entities.Span]:
    """Get all leaf spans in the trace."""
    if trace.data is None:
        return []
    spans = trace.data.spans or []
    leaf_spans_by_id = {span.span_id: span for span in spans}
    for span in spans:
        if span.parent_id:
            leaf_spans_by_id.pop(span.parent_id, None)
    return list(leaf_spans_by_id.values())


def _extract_input_text_from_span(span: mlflow_entities.Span) -> Optional[str]:
    """Extract the input text from the LLM/CHAT_MODEL span."""
    if (
        span.attributes is None
        or mlflow_tracing_constant.SpanAttributeKey.INPUTS not in span.attributes
    ):
        return None
    try:
        # See https://python.langchain.com/docs/modules/callbacks/#callback-handlers for input format
        # of CHAT_MODEL and LLM spans in LangChain
        if _span_is_type(span, mlflow_entities.SpanType.CHAT_MODEL):
            # The format of the input attribute for CHAT_MODEL is List[List[BaseMessage]]
            # e.g. [ [ { 'content': 'xxx', ... } ] ]
            return span.attributes[mlflow_tracing_constant.SpanAttributeKey.INPUTS][0][
                0
            ]["content"]
        elif _span_is_type(span, mlflow_entities.SpanType.LLM):
            # The format of the input attribute for LLM is List[str]
            # e.g. [ 'xxx', ... ]
            return span.attributes[mlflow_tracing_constant.SpanAttributeKey.INPUTS][0]
        else:
            # Span is not a LLM/CHAT_MODEL span, nothing to extract
            return None
    except Exception as e:
        _logger.debug(f"Fail to extract input text from span: {span}. Error: {e!r}")
        return None


def _extract_output_text_from_span(span: mlflow_entities.Span) -> Optional[str]:
    """Extract the output text from the LLM/CHAT_MODEL span."""
    if (
        span.attributes is None
        or mlflow_tracing_constant.SpanAttributeKey.OUTPUTS not in span.attributes
    ):
        return None
    try:
        # See https://python.langchain.com/docs/modules/callbacks/#callback-handlers for output format
        # of CHAT_MODEL and LLM spans in LangChain
        if _span_is_type(
            span, [mlflow_entities.SpanType.CHAT_MODEL, mlflow_entities.SpanType.LLM]
        ):
            # The format of the output attribute for LLM/CHAT_MODEL is a LLMResult
            # e.g. { 'generations': [ [ { 'text': 'xxx', ... } ] ], ... }
            return span.attributes[mlflow_tracing_constant.SpanAttributeKey.OUTPUTS][
                "generations"
            ][0][0]["text"]
        else:
            # Span is not a LLM/CHAT_MODEL span, nothing to extract
            return None

    except Exception as e:
        _logger.debug(f"Fail to extract output text from span: {span}. Error: {e!r}")
        return None
