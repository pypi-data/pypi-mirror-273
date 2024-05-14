import json
import os
import re
from typing import Optional, Dict, Any

from mlflow.deployments import BaseDeploymentClient, DatabricksEndpoint
from mlflow.deployments.constants import MLFLOW_DEPLOYMENT_CLIENT_REQUEST_RETRY_CODES
from mlflow.environment_variables import (
    MLFLOW_DEPLOYMENT_PREDICT_TIMEOUT,
    MLFLOW_HTTP_REQUEST_TIMEOUT,
)
from mlflow.utils import databricks_utils
from mlflow.utils.rest_utils import http_request
from requests.exceptions import HTTPError

from databricks.rag_eval import env_vars

# This is the client-id that is whitelisted by LLM proxy for RAG eval
RAG_EVAL_LLM_PROXY_CLIENT_ID = "rag-eval-built-in-judge"
CHAT_COMPLETIONS_URI = "/api/2.0/conversation/proxy/chat/completions"

# Set mlflow max retry limit to a really large number to handle 429 from LLM proxy due to rate limiting
os.environ["_MLFLOW_HTTP_REQUEST_MAX_RETRIES_LIMIT"] = "1000000"


class LlmProxyDeploymentClient(BaseDeploymentClient):

    def __init__(self, target_uri="llmproxy"):
        super().__init__(target_uri)
        self.max_retries = env_vars.RAG_EVAL_LLM_JUDGE_MAX_RETRIES_ENV_VAR.get()
        self.backoff_factor = env_vars.RAG_EVAL_LLM_JUDGE_BACKOFF_FACTOR_ENV_VAR.get()
        self.backoff_jitter = env_vars.RAG_EVAL_LLM_JUDGE_BACKOFF_JITTER_ENV_VAR.get()

    """
    mlflow deployment client plugin for interacting with the Databricks internal LLM proxy (go/llm-proxy).

    See https://mlflow.org/docs/latest/plugins.html#deployment-plugins for more details.
    """

    def create_deployment(
        self, name, model_uri, flavor=None, config=None, endpoint=None
    ):
        """
        .. warning::

           This method is not implemented for `LlmProxyDeploymentClient`.
        """
        raise NotImplementedError

    def update_deployment(
        self, name, model_uri=None, flavor=None, config=None, endpoint=None
    ):
        """
        .. warning::

           This method is not implemented for `LlmProxyDeploymentClient`.
        """
        raise NotImplementedError

    def delete_deployment(self, name, config=None, endpoint=None):
        """
        .. warning::

           This method is not implemented for `LlmProxyDeploymentClient`.
        """
        raise NotImplementedError

    def list_deployments(self, endpoint=None):
        """
        .. warning::

           This method is not implemented for `LlmProxyDeploymentClient`.
        """
        raise NotImplementedError

    def get_deployment(self, name, endpoint=None):
        """
        .. warning::

           This method is not implemented for `LlmProxyDeploymentClient`.
        """
        raise NotImplementedError

    def predict(self, deployment_name=None, inputs=None, endpoint=None):
        """
        Make a call to the LLM proxy endpoint for the given model

        :param deployment_name: this is not passed in by the mlflow deployments plugin. Used endpoint below instead
        :param inputs: The input to the LLM endpoint e.g. {"messages": [{"role": "user", "content": "What is mlflow?"}]}
        :param endpoint: the endpoint uri which is the model name such as gpt-35-turbo-0613 in llmproxy:/gpt-35-turbo-0613
        """
        return self._call_chat_completion(
            model_name=endpoint,
            model_inputs=inputs,
            timeout=MLFLOW_DEPLOYMENT_PREDICT_TIMEOUT.get(),
        )

    def get_endpoint(self, model_name):
        """
        Return the endpoint metadata for a given model name.

        TODO(ML-39567): This is hardcoded for now as the LLM proxy does not have a public API for this. Work with the LLM proxy team to expose an endpoint.

        :param model_name: the LLM model name (e.g. gpt-35-turbo-0613). See go/llmproxy for a list of supported models.
        """
        return {
            "name": "llm-proxy-chat-completions",
            "endpoint_type": "llm/v1/chat",
            "model": {"name": model_name, "provider": "llmproxy"},
            "endpoint_url": CHAT_COMPLETIONS_URI,
        }

    def _call_chat_completion(
        self,
        *,
        model_name,
        model_inputs: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
    ):
        """
        Calls the llm proxy endpoint with the given payload and parameters.

        :param model_name: the name of the model deployment (e.g. gpt-35-turbo-0613)
        :param model_inputs: the inputs to the LLM
        :param timeout: the timeout for the request
        :return: the response dictionary from the result of the LLM proxy call
        """

        request_body_json = {
            "@method": "openAiServiceChatCompletionRequest",
            "params": model_inputs,
            "model": model_name,
            # The client-id is used by LLM proxy to identify the client, collect metrics and enforce rate limits
            "metadata": {"clientId": RAG_EVAL_LLM_PROXY_CLIENT_ID},
            "apiVersion": "2024-03-01-preview",  # Required to address [ML-40175]
        }

        """
        An example request to LLM Prox as per go/llmproxy

        curl -X POST \
          "https://<HOST_NAME>}/api/2.0/conversation/proxy/chat/completions" \
          --header "Authentication: Bearer <PAT TOKEN>" \
          --data '{
            "@method": "openAiServiceChatCompletionRequest",
            "model": "gpt-4-1106preview",
            "apiVersion": "2024-03-01-preview",
            "params": {
              "messages": [{"role": "user", "content": "What is mlflow?"}]
            }
            "metadata": {
              "clientId": "rag-eval-built-in-judge"
            }
          }
        """
        response = http_request(
            # TODO(ML-39565) Adopt non-token based authentication to talk to LLM Proxy
            host_creds=databricks_utils.get_databricks_host_creds(),
            endpoint=CHAT_COMPLETIONS_URI,
            method="POST",  # LLM proxy chat completions only support POST
            timeout=(MLFLOW_HTTP_REQUEST_TIMEOUT.get() if timeout is None else timeout),
            max_retries=self.max_retries,
            backoff_factor=self.backoff_factor,
            backoff_jitter=self.backoff_jitter,
            raise_on_status=False,
            retry_codes=MLFLOW_DEPLOYMENT_CLIENT_REQUEST_RETRY_CODES,
            json=request_body_json,
        )

        # sanitize the response error message to remove any internal information such as the LLM proxy endpoint url
        try:
            response.raise_for_status()
        except HTTPError as e:
            sanitized_message = self._sanitize_error_message(str(e))
            raise HTTPError(sanitized_message) from None

        # mlflow metrics evaluation expects only cares about the json response under the "completion" field
        return DatabricksEndpoint(json.loads(response.json()["completion"]))

    @staticmethod
    def _sanitize_error_message(error_msg: str) -> str:
        """
        Sanitize the error message by removing any sensitive info that we don't want to surface to our customers

        Remove any local URLs of the following forms that can be returned by the LLM proxy such as
        "for url: <some url>/api/2.0/conversation/proxy/chat/completions+optional parameters"
        """

        error_message = re.sub(
            r"(for url: )?(http|https)://.*/api/2.0/conversation/proxy/chat/completions(\?.*&?([^= ]+)=([^& ]*))?",
            "",
            error_msg,
        )

        return error_message.strip()
