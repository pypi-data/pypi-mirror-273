"""
Introduces main Context class and the framework to specify different specialized
contexts.
"""

from __future__ import annotations

import functools
import inspect
import logging
from abc import ABC, abstractmethod

from databricks.rag_eval.clients import llmjudge

import mlflow
from mlflow.utils import databricks_utils

from databricks.rag_eval.clients.llmjudge import llm_judge_client


_logger = logging.getLogger(__name__)


class Context(ABC):
    """
    Abstract class for execution context.
    """

    @abstractmethod
    def clear_context(self) -> None:
        """
        Clears the context and frees up any resources as needed.
        """
        pass

    @abstractmethod
    def display_html(self, html: str) -> None:
        """
        Displays HTML in the current execution context.
        """
        pass

    @abstractmethod
    def get_llm_judge_client(self) -> llmjudge.LlmJudgeClient:
        """
        Gets the LLM Judge client for the current session.
        """
        pass


class NoneContext(Context):
    """
    A context that does nothing.
    """

    def clear_context(self) -> None:
        raise AssertionError("Context is not set")

    def display_html(self, html: str) -> None:
        raise AssertionError("Context is not set")

    def get_llm_judge_client(self) -> llmjudge.LlmJudgeClient:
        raise AssertionError("Context is not set")


class DatabricksContext(Context):
    """
    Context for eval execution.

    NOTE: This class is not covered by unit tests and is meant to be tested through
    smoke tests that run this code on an actual Databricks cluster.
    """

    @classmethod
    def _get_dbutils(cls):
        """
        Returns an instance of dbutils.
        """
        try:
            from databricks.sdk.runtime import dbutils

            return dbutils
        except ImportError:
            import IPython

            dbutils = IPython.get_ipython().user_ns["dbutils"]
        return dbutils

    def __init__(self):
        host_creds = databricks_utils.get_databricks_host_creds()
        api_url = host_creds.host
        api_token = host_creds.token

        self._dbutils = self._get_dbutils()
        self._llm_judge_client = llm_judge_client.LlmJudgeClient(
            api_url=api_url,
            api_token=api_token,
        )

        # Set MLflow model registry to Unity Catalog
        mlflow.set_registry_uri("databricks-uc")

    def clear_context(self) -> None:
        pass

    def display_html(self, html) -> None:
        # pylint: disable=protected-access
        self._dbutils.notebook.displayHTML(html)

    def get_llm_judge_client(self) -> llm_judge_client.LlmJudgeClient:
        return self._llm_judge_client


class ContextSingleton:
    """
    A singleton context
    """

    _instance: "ContextSingleton" = None

    def __new__(cls):
        if cls._instance is None:
            # Forward to the "normal" __new__ which properly constructs the object
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._context_impl = NoneContext()

    def set(self, context_impl: Context) -> None:
        assert not self.active
        self._context_impl = context_impl

    def clear(self) -> None:
        self._context_impl.clear_context()
        self._context_impl = NoneContext()

    @property
    def active(self) -> bool:
        return not isinstance(self._context_impl, NoneContext)

    def display_html(self, html: str) -> None:
        self._context_impl.display_html(html)

    @property
    def llm_judge_client(self) -> llmjudge.LlmJudgeClient:
        return self._context_impl.get_llm_judge_client()


context: ContextSingleton = ContextSingleton()


def eval_context(func):
    """
    Decorator for wrapping all eval APIs with setup and closure logic.

    The wrapper will set up an active DatabricksContext if there isn't one already,
    and will also instrument the API call to add usage logging by timing it and
    recording the parameters and errors (if any).

    :param func: eval function to wrap
    :return: return value of func
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not context.active:
            context.set(DatabricksContext())

        error = None
        result = None

        parameters = inspect.signature(func).parameters
        # Get all the parameters with default values from the method signature.
        # If a parameter does not have default value, it will not be included in the `full_kwargs`.
        full_kwargs = {
            param_name: parameters[param_name].default
            for param_name in parameters
            if parameters[param_name].default != inspect.Parameter.empty
        }
        # Merge the parameters default values with the values passed in by the user.
        full_kwargs.update(kwargs)

        # Do any preprocessing of the args here

        try:
            result = func(*args, **full_kwargs)
        except Exception as e:  # pylint: disable=broad-except
            error = e
        finally:
            # Raise the original error if there was one, otherwise return
            if error is not None:
                raise error
            else:
                return result  # pylint: disable=lost-exception

    return wrapper
