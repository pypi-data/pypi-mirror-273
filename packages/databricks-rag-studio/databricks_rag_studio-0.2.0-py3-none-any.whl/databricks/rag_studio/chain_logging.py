import mlflow
import os
from typing import Optional, Union, Dict, Any
from contextlib import contextmanager
from mlflow.utils.annotations import deprecated
from mlflow.models import ModelSignature
from mlflow.models.model import ModelInfo
from mlflow.types import DataType
from mlflow.types.schema import Schema, ColSpec, Object, Array, Property
from databricks.rag.version import VERSION as RAG_SERVING_VERSION


@contextmanager
def _start_run_or_reuse_active_run():
    """
    Context manager that:
     - returns the active run ID, if exists
     - otherwise start a new mlflow run, and return the run id.
    """
    active_run = mlflow.active_run()
    if active_run:
        yield active_run.info.run_id
    else:
        with mlflow.start_run() as run:
            yield run.info.run_id


@deprecated("Use `mlflow.langchain.log_model` instead")
def log_model(
    *,
    code_path: str,
    config: Optional[Union[str, Dict[str, Any]]] = None,
    **kwags,
) -> ModelInfo:
    """
    Logs chain code (located at the specified ``code_path``) and configurations.

    :param code_path: The string notebook or file path to the chain code.
    :param config: Python dictionary or path to the configs used to build the chain model.

    :return: A ModelInfo instance that contains the metadata of the logged model.

    Example:

    ```

    from databricks import rag_studio

    model = rag_studio.log_model(
        code_path="ai-bot/chain.py",
        config="ai-bot/chain_config.yml",
    )

    question = {
        "messages": [
            {
                "role": "user",
                "content": "What is Retrieval-augmented Generation?",
            }
        ]
    }

    model.invoke(question)

    ```

    """
    import langchain
    import langchain_core
    import langchain_community
    import databricks.vector_search

    config_path = kwags.get("config_path", None)
    if config_path is not None and (
        not isinstance(config_path, str) or not os.path.exists(config_path)
    ):
        raise ValueError(f"Chain config file {config_path} does not exist")

    if config is not None:
        if config_path is not None:
            raise ValueError(
                "Cannot specify both 'config' and 'config_path' arguments."
            )
        config_path = config

    if not isinstance(code_path, str):
        raise ValueError(f"Chain file {code_path} does not exist.")

    chain_path = os.path.abspath(code_path)
    if not os.path.exists(chain_path):
        raise ValueError(
            f"Specified chain file {code_path} resolved to full path {chain_path} does not exist."
        )

    with _start_run_or_reuse_active_run():
        input_example = {
            "messages": [
                {
                    "role": "user",
                    "content": "What is Retrieval-augmented Generation?",
                }
            ]
        }
        signature = ModelSignature(
            inputs=Schema(
                [
                    ColSpec(
                        type=Array(
                            Object(
                                [
                                    Property("role", DataType.string),
                                    Property("content", DataType.string),
                                ]
                            ),
                        ),
                        name="messages",
                    )
                ]
            ),
            outputs=Schema(
                [
                    ColSpec(name="id", type=DataType.string),
                    ColSpec(name="object", type=DataType.string),
                    ColSpec(name="created", type=DataType.long),
                    ColSpec(name="model", type=DataType.string),
                    ColSpec(name="choices", type=DataType.string),
                    ColSpec(name="usage", type=DataType.string),
                ]
            ),
        )

        return mlflow.langchain.log_model(
            lc_model=chain_path,
            artifact_path="chain",
            pip_requirements=[
                "mlflow>=2.12.2",
                f"langchain=={langchain.__version__}",
                f"langchain-core=={langchain_core.__version__}",
                f"langchain-community=={langchain_community.__version__}",
                f"databricks-vectorsearch=={databricks.vector_search.__version__}",
                f"https://ml-team-public-read.s3.us-west-2.amazonaws.com/wheels/rag-serving/uqr082kj-3c87-40b1-b04c-bb1977254aa3/databricks_rag_serving-{RAG_SERVING_VERSION}-py3-none-any.whl",
            ],
            signature=signature,
            input_example=input_example,
            example_no_conversion=True,
            model_config=config_path if config_path else None,
        )
