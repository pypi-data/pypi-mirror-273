"""
This module defines the RagEvaluationDataset class, which is transforms mlflow.evaluate inputs into entities used by the evaluation harness.
"""

from typing import List

import pandas as pd
from mlflow.models import evaluation as mlflow_evaluation

from databricks.rag_eval.evaluation import entities
from databricks.rag_eval.evaluation import schemas
from databricks.rag_eval.mlflow import dataframe_wrapper


class RagEvaluationDataset:
    """Represents the data passed to mlflow.evaluate"""

    def __init__(self, df: pd.DataFrame):
        self._input_df = dataframe_wrapper.EvaluationDataframe(df)
        self._input_df.validate()

    @property
    def eval_items(self) -> List[entities.EvalItem]:
        """Returns a list of EvalItems to evaluate."""
        normalized_df = self._input_df.normalized_df
        return normalized_df.apply(entities.EvalItem.from_pd_series, axis=1).tolist()

    @classmethod
    def _validate_mlflow_dataset(cls, ds: mlflow_evaluation.EvaluationDataset):
        """Validates an MLflow evaluation dataset."""
        features_df = ds.features_data
        if ds.predictions_data is not None:
            assert features_df.shape[0] == ds.predictions_data.shape[0], (
                f"Features data and predictions must have the same number of rows. "
                f"Features: {features_df.shape[0]}, Predictions: {ds.predictions_data.shape[0]}"
            )

    @classmethod
    def from_mlflow_dataset(
        cls, ds: mlflow_evaluation.EvaluationDataset
    ) -> "RagEvaluationDataset":
        """Creates an instance of the class from an MLflow evaluation dataset and model predictions."""
        cls._validate_mlflow_dataset(ds)
        df = ds.features_data.copy()
        if ds.predictions_data is not None:
            df[schemas.RESPONSE_COL] = ds.predictions_data
        return cls(df)
