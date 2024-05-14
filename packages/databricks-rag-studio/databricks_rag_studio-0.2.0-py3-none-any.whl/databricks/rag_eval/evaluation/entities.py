"""Entities for evaluation."""

import dataclasses
import functools
import uuid
from typing import TypeAlias, Optional, Collection, List, Mapping, Dict, Any

import mlflow.entities as mlflow_entities
import pandas as pd

from databricks.rag_eval.config import assessment_config
from databricks.rag_eval.evaluation import schemas


@dataclasses.dataclass
class Chunk:
    doc_uri: Optional[str] = None
    content: Optional[str] = None

    @classmethod
    def from_dict(
        cls, retrieval_context_entry: Optional[Dict[str, Any]]
    ) -> Optional["Chunk"]:
        """Construct a Chunk from a dictionary optionally containing doc_uri and content. If the input is None, returns None."""
        if retrieval_context_entry is None:
            return None
        return cls(
            doc_uri=retrieval_context_entry.get(schemas.DOC_URI_COL),
            content=retrieval_context_entry.get(schemas.CHUNK_CONTENT_COL),
        )


class RetrievalContext(List[Optional[Chunk]]):
    def __init__(self, chunks: Collection[Optional[Chunk]]):
        super().__init__(chunks)

    def concat_chunk_content(self, delimiter: str = "\n") -> Optional[str]:
        """
        Concatenate the non-empty content of the chunks to a string with the given delimiter.
        Return None if all the contents are empty.
        """
        non_empty_contents = [
            chunk.content for chunk in self if chunk is not None and chunk.content
        ]
        return delimiter.join(non_empty_contents) if non_empty_contents else None

    def get_doc_uris(self) -> List[str]:
        """Get the list of doc URIs in the retrieval context."""
        return [chunk.doc_uri for chunk in self if chunk is not None]

    def to_output_dict(self) -> List[Dict[str, str]]:
        """Convert the RetrievalContext to a list of dictionaries with the schema defined in schemas.CHUNK_SCHEMA."""
        return [
            (
                {
                    schemas.DOC_URI_COL: chunk.doc_uri,
                    schemas.CHUNK_CONTENT_COL: chunk.content,
                }
                if chunk is not None
                else None
            )
            for chunk in self
        ]


@dataclasses.dataclass
class Rating:
    bool_value: Optional[bool]
    double_value: Optional[float]
    rationale: Optional[str]
    error_message: Optional[str]

    @classmethod
    def build(
        cls, *, bool_value: bool, double_value: float, rationale: str
    ) -> "Rating":
        """Build a normal Rating with a boolean value, a double value, and a rationale."""
        return cls(
            bool_value=bool_value,
            double_value=double_value,
            rationale=rationale,
            error_message=None,
        )

    @classmethod
    def error(cls, error_message: str) -> "Rating":
        """Build an error Rating with an error message."""
        return cls(
            bool_value=None,
            double_value=None,
            rationale=None,
            error_message=error_message,
        )


PositionalRating: TypeAlias = Mapping[int, Rating]
"""
A mapping from position to rating.
Position refers to the position of the chunk in the retrieval context.
It is used to represent the ratings of the chunks in the retrieval context.
"""


@functools.total_ordering
@dataclasses.dataclass
class EvalItem:
    """
    Represents a row in the evaluation dataset. It contains information needed to evaluate a question.
    """

    question_id: str
    question: str
    answer: Optional[str]
    retrieval_context: Optional[RetrievalContext]
    ground_truth_answer: Optional[str]
    ground_truth_retrieval_context: Optional[RetrievalContext]
    trace: Optional[mlflow_entities.Trace]

    @property
    def concatenated_retrieval_context(self) -> Optional[str]:
        """Get the concatenated content of the retrieval context.
        Return None if there is no non-empty retrieval context content."""
        return (
            self.retrieval_context.concat_chunk_content()
            if self.retrieval_context
            else None
        )

    @classmethod
    def from_pd_series(cls, series: pd.Series):
        """
        Create an EvalItem from a row of MLflow EvaluationDataset data.
        """
        retrieved_context = (
            RetrievalContext(
                [
                    (
                        Chunk.from_dict(chunk_data)
                        if isinstance(chunk_data, dict)
                        else Chunk(doc_uri=chunk_data)
                    )
                    for chunk_data in series[schemas.RETRIEVED_CONTEXT_COL]
                ]
            )
            if schemas.RETRIEVED_CONTEXT_COL in series
            else None
        )

        expected_retrieved_context = (
            RetrievalContext(
                [
                    (
                        Chunk.from_dict(chunk_data)
                        if isinstance(chunk_data, dict)
                        else Chunk(doc_uri=chunk_data)
                    )
                    for chunk_data in series[schemas.EXPECTED_RETRIEVED_CONTEXT_COL]
                ]
            )
            if schemas.EXPECTED_RETRIEVED_CONTEXT_COL in series
            else None
        )

        question = series[schemas.REQUEST_COL]
        question_id = series.get(schemas.REQUEST_ID_COL, str(uuid.uuid4()))

        return cls(
            question_id=question_id,
            question=question,
            answer=series.get(schemas.RESPONSE_COL),
            retrieval_context=retrieved_context,
            ground_truth_answer=series.get(schemas.EXPECTED_RESPONSE_COL),
            ground_truth_retrieval_context=expected_retrieved_context,
            trace=series.get(schemas.TRACE_COL),
        )

    def __eq__(self, other):
        if not hasattr(other, "question_id"):
            return NotImplemented
        return self.question_id == other.question_id

    def __lt__(self, other):
        if not hasattr(other, "question_id"):
            return NotImplemented
        return self.question_id < other.question_id


@dataclasses.dataclass
class AssessmentResult:
    """Holds the result of an assessment."""

    assessment_name: str
    assessment_type: assessment_config.AssessmentType


@dataclasses.dataclass
class AnswerAssessmentResult(AssessmentResult):
    """Holds the result of an answer assessment."""

    rating: Rating
    assessment_type: assessment_config.AssessmentType = dataclasses.field(
        init=False, default=assessment_config.AssessmentType.ANSWER
    )


@dataclasses.dataclass
class RetrievalAssessmentResult(AssessmentResult):
    """Holds the result of a retrieval assessment."""

    positional_rating: PositionalRating
    assessment_type: assessment_config.AssessmentType = dataclasses.field(
        init=False, default=assessment_config.AssessmentType.RETRIEVAL
    )


@dataclasses.dataclass
class AssessmentLog:
    """Holds the assessment logs for a single eval item."""

    eval_item: EvalItem
    assessment_results: Collection[AssessmentResult]
    """
    A collection of AssessmentResult.
    Assessment name is should be unique for each eval item.
    """

    def __post_init__(self):
        if not self.assessment_results:
            self.assessment_results = []


@dataclasses.dataclass
class EvalResult:
    """Holds the result of the evaluation for an eval item."""

    eval_item: EvalItem
    assessment_results: Collection[AssessmentResult]

    request_token_count: Optional[int]
    """Request token count."""
    response_token_count: Optional[int]
    """Response token count."""
    total_input_token_count: Optional[int]
    """Total input tokens across all spans in the trace."""
    total_output_token_count: Optional[int]
    """Total output tokens across all spans in the trace."""
    total_token_count: Optional[int]
    """Total tokens across all spans in the trace."""
    exact_match: Optional[bool]
    latency_seconds: Optional[float]
    ground_truth_retrieval_metrics: Mapping[str, float]
    """
    Ground truth retrieval metrics, such as precision/recall, etc.
    It is computed by comparing the ground truth retrieval context with the retrieval context.

    metric_name -> score, e.g. {precision: 0.5, recall: 0.1}
    """
    llm_judged_retrieval_metrics: Mapping[str, float]
    """
    LLM-judged retrieval metrics.
    e.g. Use the "context_relevance" assessment result to calculate precision of the retrieval.

    metric_name -> score, e.g. {precision: 0.5}
    """

    def to_pd_series(self) -> pd.Series:
        """Converts the EvalResult to a flattened pd.Series."""
        # Extracting relevant fields from eval_item and assessment_results
        inputs = {
            schemas.REQUEST_ID_COL: self.eval_item.question_id,
            schemas.REQUEST_COL: self.eval_item.question,
            schemas.RESPONSE_COL: self.eval_item.answer,
            schemas.EXPECTED_RETRIEVED_CONTEXT_COL: (
                self.eval_item.ground_truth_retrieval_context.to_output_dict()
                if self.eval_item.ground_truth_retrieval_context
                else None
            ),
            schemas.EXPECTED_RESPONSE_COL: self.eval_item.ground_truth_answer,
            schemas.RETRIEVED_CONTEXT_COL: (
                self.eval_item.retrieval_context.to_output_dict()
                if self.eval_item.retrieval_context
                else None
            ),
            schemas.TRACE_COL: self.eval_item.trace,
        }

        # Flatten the assessment results into the series
        assessments: Dict[str, schemas.ASSESSMENT_RESULT_TYPE] = {}
        for assessment in self.assessment_results:
            if isinstance(assessment, AnswerAssessmentResult):
                prefix = (
                    schemas.LLM_JUDGED_RESPONSE_METRIC_COL_PREFIX
                    + assessment.assessment_name
                )
                assessments[f"{prefix}_rating"] = assessment.rating.bool_value
                assessments[f"{prefix}_rationale"] = assessment.rating.rationale
                assessments[f"{prefix}_error_message"] = assessment.rating.error_message
            elif isinstance(assessment, RetrievalAssessmentResult):
                prefix = (
                    schemas.LLM_JUDGED_RETRIEVAL_METRIC_COL_PREFIX
                    + assessment.assessment_name
                )
                ratings_by_context_position = [
                    rating for _, rating in sorted(assessment.positional_rating.items())
                ]
                assessments[f"{prefix}_ratings"] = [
                    rating.bool_value for rating in ratings_by_context_position
                ]
                assessments[f"{prefix}_rationales"] = [
                    rating.rationale for rating in ratings_by_context_position
                ]
                assessments[f"{prefix}_error_messages"] = [
                    rating.error_message for rating in ratings_by_context_position
                ]

        metrics: Dict[str, schemas.METRIC_RESULT_TYPE] = {
            **{
                f"{schemas.LLM_JUDGED_RETRIEVAL_METRIC_COL_PREFIX}{metric_name}": metric_value
                for metric_name, metric_value in self.llm_judged_retrieval_metrics.items()
            },
            **{
                f"{schemas.GROUND_TRUTH_RETRIEVAL_METRIC_COL_PREFIX}{metric_name}": metric_value
                for metric_name, metric_value in self.ground_truth_retrieval_metrics.items()
            },
            schemas.REQUEST_TOKEN_COUNT: self.request_token_count,
            schemas.RESPONSE_TOKEN_COUNT: self.response_token_count,
            schemas.TOTAL_INPUT_TOKEN_COUNT_COL: self.total_input_token_count,
            schemas.TOTAL_OUTPUT_TOKEN_COUNT_COL: self.total_output_token_count,
            schemas.TOTAL_TOKEN_COUNT_COL: self.total_token_count,
            schemas.LATENCY_SECONDS_COL: self.latency_seconds,
        }
        # Remove None values in metrics
        metrics = {key: value for key, value in metrics.items() if value is not None}

        # Merge dictionaries and convert to pd.Series
        combined_data = {**inputs, **assessments, **metrics}
        return pd.Series(combined_data)
