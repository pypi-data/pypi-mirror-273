from databricks.rag_eval.clients.llmproxy.llm_proxy_client import (
    LlmProxyDeploymentClient,
)


# The following methods are required by mlflow deployment plugins and must be defined at the package level referenced
# by the "mlflow.deployments" entry point in setup.py.
# See https://mlflow.org/docs/latest/plugins.html#deployment-plugins for more details
def target_help():
    return "This mlflow deployment plugin integrates with the internal Databricks LLM Proxy (go/llmproxy)."


def run_local(target, name, model_uri, flavor=None, config=None):
    # The LLM proxy deployment plugin does not support running locally
    raise NotImplementedError


__all__ = ["target_help", "run_local", "LlmProxyDeploymentClient"]
