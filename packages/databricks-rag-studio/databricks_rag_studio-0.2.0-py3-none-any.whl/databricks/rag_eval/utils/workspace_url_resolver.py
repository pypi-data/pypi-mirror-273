import mlflow.entities


class WorkspaceUrlResolver:
    """
    A class to resolve URLs for different entities in a workspace.
    """

    def __init__(self, workspace_url):
        """
        :param instance_name: Databricks workspace instance name (e.g. e2-dogfood.staging.cloud.databricks.com)
        :param workspace_id: ID of this workspace
        """
        self._workspace_url = workspace_url

    def _get_full_url(self, path):
        return f"https://{self._workspace_url}/{path}/"

    def resolve_url_for_mlflow_run(self, info: mlflow.entities.RunInfo) -> str:
        """Resolve the URL for a MLflow run."""
        path = f"ml/experiments/{info.experiment_id}/runs/{info.run_id}"
        return self._get_full_url(path)

    def resolve_url_for_mlflow_experiment(self, info: mlflow.entities.RunInfo) -> str:
        """Resolve the URL for a MLflow experiment."""
        path = f"ml/experiments/{info.experiment_id}"
        return self._get_full_url(path)
