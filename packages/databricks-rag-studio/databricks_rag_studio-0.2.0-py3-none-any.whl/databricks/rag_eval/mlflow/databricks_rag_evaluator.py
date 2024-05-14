import textwrap
from typing import Dict, Any, Optional

import mlflow
import pandas as pd
from mlflow import models as mlflow_models
from mlflow.models import evaluation as mlflow_evaluation
from mlflow.models.evaluation import artifacts as mlflow_artifacts
from mlflow.utils import mlflow_tags

from databricks.rag_eval import context, constants
from databricks.rag_eval.config import evaluation_config
from databricks.rag_eval.evaluation import harness
from databricks.rag_eval.mlflow import datasets, mlflow_log_metrics
from databricks.rag_eval.utils import workspace_url_resolver


def _log_pandas_df_artifact(pandas_df, artifact_name):
    """
    Logs a pandas DataFrame as a JSON artifact, then returns an EvaluationArtifact object.
    """
    mlflow_artifact_name = f"{artifact_name}.json"
    mlflow.log_table(pandas_df, mlflow_artifact_name)
    return mlflow_artifacts.JsonEvaluationArtifact(
        uri=mlflow.get_artifact_uri(mlflow_artifact_name),
    )


def _emit_usage_instructions(run_id, context):
    """
    Displays instructions to the user on what to do after running `mlflow.evaluate`.
    """
    run = mlflow.get_run(run_id)
    if mlflow_tags.MLFLOW_DATABRICKS_WORKSPACE_URL in run.data.tags:
        # Include Databricks URLs in the displayed message.
        workspace_url = run.data.tags[mlflow_tags.MLFLOW_DATABRICKS_WORKSPACE_URL]
        resolver = workspace_url_resolver.WorkspaceUrlResolver(workspace_url)
        experiment_url = resolver.resolve_url_for_mlflow_experiment(run.info)
        run_url = resolver.resolve_url_for_mlflow_run(run.info)

        context.display_html(
            textwrap.dedent(
                f"""
            <b>Evaluation completed.</b><br><br>

            Aggregate metrics are available in <code>mlflow.evaluate(...).metrics</code>.<br>
            Per-row evaluation results are available in <code>mlflow.evaluate(...).tables['eval_results']</code>.<br><br>

            Metrics and evaluation results are logged to MLflow, and can be viewed from the <a href='{run_url}'>MLflow run page</a>,
            or the "Evaluation" tab of the <a href='{experiment_url}'>Experiment page</a>.
            """
            )
        )
    else:
        print(
            textwrap.dedent(
                """
            Evaluation completed.

            Aggregate metrics are available in mlflow.evaluate(...).metrics.
            Per-row evaluation results are available in mlflow.evaluate(...).tables['eval_results'].

            Metrics and evaluation results are logged to MLflow, and can be viewed from the MLflow run page,
            or the "Evaluation" tab of the Experiment page.
                    """
            )
        )


class DatabricksRagEvaluator(mlflow_evaluation.base.ModelEvaluator):
    def can_evaluate(self, *, model_type, evaluator_config, **kwargs) -> bool:
        """
        See parent class docstring.
        """
        return model_type == "databricks-rag"

    @context.eval_context
    def evaluate(
        self,
        *,
        model_type,
        dataset,
        run_id,
        evaluator_config: Optional[Dict[str, Any]] = None,
        model=None,
        custom_metrics=None,
        extra_metrics=None,
        custom_artifacts=None,
        baseline_model=None,
        predictions=None,
        **kwargs,
    ):
        """
        Runs Databricks RAG evaluation on the provided dataset.

        The following arguments are supported:
        - model_type: Must be "databricks-rag".
        - dataset
        - run_id

        For more details, see parent class docstring.
        """
        eval_dataset = datasets.RagEvaluationDataset.from_mlflow_dataset(dataset)
        config_str = evaluator_config and evaluator_config.get(
            constants.EVALUATOR_CONFIG_KEY_NAME, None
        )
        config = evaluation_config.EvaluationConfig.from_yaml(
            config_str or evaluation_config.default_config()
        )

        eval_results = harness.run(
            eval_items=eval_dataset.eval_items, config=config, model=model
        )

        mlflow_metrics = mlflow_log_metrics.generate_mlflow_metrics(eval_results)
        mlflow.log_metrics(mlflow_metrics)

        eval_results_df = pd.DataFrame(
            [result.to_pd_series() for result in eval_results]
        )

        eval_results_artifact = _log_pandas_df_artifact(eval_results_df, "eval_results")
        result = mlflow_models.EvaluationResult(
            metrics=mlflow_metrics,
            artifacts={"eval_results": eval_results_artifact},
        )
        _emit_usage_instructions(result._run_id, context.context)
        return result
