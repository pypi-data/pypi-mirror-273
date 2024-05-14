# TODO[]: remove this module after legacy builtin judges are removed.

import pandas as pd


def no_op(**kwargs):
    """
    No-op MLflow metrics that simply returns NULL scores.
    """
    import mlflow
    from mlflow.metrics import MetricValue

    def _no_op_eval_fn(predictions: pd.Series) -> MetricValue:
        size = len(predictions)
        return MetricValue(scores=[None] * size, justifications=[None] * size)

    return mlflow.models.make_metric(eval_fn=_no_op_eval_fn, greater_is_better=False)
