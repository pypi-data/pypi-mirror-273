""" This module defines classes that wrap pandas DataFrames used in evaluation.

Wrappers handle data validation and normalization.

This currently only includes mlflow.models.evaluation.EvaluationDataset.features_data.
 """

from typing import Iterable, Mapping, Set

import pandas as pd
from abc import ABC
from typing import Any

from databricks.rag_eval.evaluation import schemas


class _InputColumn(ABC):
    """Represents a column in the MLflow EvaluationDataset features DataFrame."""

    name: str
    required: bool

    @classmethod
    def validate(cls, df: pd.DataFrame) -> None:
        if cls.required and cls.name not in df.columns:
            raise ValueError(
                f'Column "{cls.name}" is required but not found in the input DataFrame.'
            )
        if cls.name not in df.columns:
            return
        col = df[cls.name]
        if cls.required:
            for index, value in col.items():
                if value is None:
                    raise ValueError(
                        f'Column "{cls.name}" is required and must not contain null values. '
                        f"Got null at row: {index}."
                    )


class _StringColumn(_InputColumn):
    @classmethod
    def validate(cls, df: pd.DataFrame):
        super().validate(df)

        # Skip validation if the column is not present
        if cls.name not in df.columns:
            return

        for index, value in df[cls.name].items():
            if value is None:
                # Null values are valid in optional column.
                continue
            if not isinstance(value, str):
                raise ValueError(
                    f"Column '{cls.name}' must contain only string values. "
                    f"Got '{value}' at row: {index}."
                )


def _mapping_has_field(
    mapping: Mapping[str, Any],
    field_name: str,
    expected_type: type,
    required: bool = False,
) -> bool:
    field_value = mapping.get(field_name)
    if field_value is None:
        return not required
    return isinstance(field_value, expected_type)


class _ContextColumn(_InputColumn):
    @classmethod
    def _chunk_is_valid(cls, chunk: Any) -> bool:
        if chunk is None:
            return True  # Each chunk can be None
        if isinstance(chunk, str):
            return True  # Chunk can be just a doc_uri (str)
        if not isinstance(chunk, Mapping):
            return False  # Otherwise, chunk must be a map-like object
        keys = set(chunk.keys())
        # Check types of doc_uri and content
        if not _mapping_has_field(chunk, schemas.DOC_URI_COL, str, required=False):
            return False
        if not _mapping_has_field(
            chunk, schemas.CHUNK_CONTENT_COL, str, required=False
        ):
            return False
        # Invalid if dictionary contains any other keys
        if len(keys - {schemas.DOC_URI_COL, schemas.CHUNK_CONTENT_COL}) > 0:
            return False
        return True

    @classmethod
    def validate(cls, df: pd.DataFrame):
        super().validate(df)

        # Skip validation if the column is not present
        if cls.name not in df.columns:
            return

        for index, value in df[cls.name].items():
            if value is None:
                # Null values are valid in optional column.
                continue
            # Check that the value is an iterable of valid chunks. Strings, Mappings, and non-iterables are not allowed.
            if (
                isinstance(value, str)
                or isinstance(value, Mapping)
                or not (
                    isinstance(value, Iterable)
                    and all(cls._chunk_is_valid(item) for item in value)
                )
            ):
                raise ValueError(
                    f"Column '{cls.name}' must contain values of the form [doc_uri: str], [{{'doc_uri': str}}], or [{{'doc_uri': str}}, {{'content': str}}]. "
                    f"Got '{value}' at row: {index}."
                )


class _RequestIdCol(_StringColumn):
    name = schemas.REQUEST_ID_COL
    required = False


class _RequestCol(_StringColumn):
    name = schemas.REQUEST_COL
    required = True


class _ExpectedRetrievedContextCol(_ContextColumn):
    name = schemas.EXPECTED_RETRIEVED_CONTEXT_COL
    required = False


class _ExpectedResponseCol(_StringColumn):
    name = schemas.EXPECTED_RESPONSE_COL
    required = False


class _ResponseCol(_StringColumn):
    name = schemas.RESPONSE_COL
    required = False


class _RetrievedContextCol(_ContextColumn):
    name = schemas.RETRIEVED_CONTEXT_COL
    required = False


class _TraceCol(_InputColumn):
    name = schemas.TRACE_COL
    required = False

    @classmethod
    def validate(cls, df: pd.DataFrame):
        super().validate(df)
        # TODO(ML-41086): Validate data


class EvaluationDataframe:
    """Wraps an MLflow EvaluationDataset features DataFrame, providing data validation and normalization."""

    COLS = [
        _RequestIdCol,
        _RequestCol,
        _ExpectedRetrievedContextCol,
        _ExpectedResponseCol,
        _ResponseCol,
        _RetrievedContextCol,
        _TraceCol,
    ]

    def __init__(self, df: pd.DataFrame):
        self._df = df
        self._normalized_df = None

    def validate(self):
        """Validates the input DataFrame. This method is somewhat expensive, since each row of data is validated."""
        for col in self.COLS:
            col.validate(self._df)

    def _normalize(self) -> pd.DataFrame:
        """Returns a normalized copy of the DataFrame. You must call validate() before calling this method."""
        if self._normalized_df is None:
            self._normalized_df = self._df.copy()
            # TODO(ML-40872): Implement input normalization
        return self._normalized_df

    @classmethod
    def required_column_names(cls) -> Set[str]:
        return {col.name for col in cls.COLS if col.required}

    @classmethod
    def optional_column_names(cls) -> Set[str]:
        return {col.name for col in cls.COLS if not col.required}

    @property
    def normalized_df(self) -> pd.DataFrame:
        """Returns a normalized DataFrame. You must call validate() before accessing this property."""
        return self._normalize()
