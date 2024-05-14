from typing import List, Optional
import mlflow
from databricks.rag_studio.sdk_utils.permissions_checker import (
    _check_manage_permissions_on_deployment,
)
from databricks.rag_studio.client.rest_client import (
    get_chain_deployments as rest_get_chain_deployments,
    create_review_artifacts as rest_create_review_artifacts,
    set_review_instructions as rest_set_review_instructions,
    get_review_instructions as rest_get_review_instructions,
)
from databricks.sdk import WorkspaceClient
from databricks.rag.unpacking import unpack_and_split_payloads

_TRACES_FILE_PATH = "traces.json"


def _get_table_name(auto_capture_config):
    catalog_name = auto_capture_config.catalog_name
    schema_name = auto_capture_config.schema_name
    table_name = auto_capture_config.state.payload_table.name
    return f"`{catalog_name}`.`{schema_name}`.`{table_name}`"


def _get_inference_table_from_serving(model_name, serving_endpoint_name):
    w = WorkspaceClient()
    serving_endpoint = w.serving_endpoints.get(serving_endpoint_name)
    if (
        serving_endpoint.config is None
        or serving_endpoint.config.auto_capture_config is None
    ):
        raise ValueError(
            f"The provided {model_name} doesn't have any inference table configured. "
            "Please update the endpoint to capture payloads to an inference table"
        )

    auto_capture_config = serving_endpoint.config.auto_capture_config
    if (
        auto_capture_config.catalog_name is None
        or auto_capture_config.schema_name is None
    ):
        raise ValueError(
            f"The provided {model_name} doesn't have any inference table configured. "
            "Please update the endpoint to capture payloads to an inference table"
        )

    return _get_table_name(auto_capture_config)


def _generate_review_experiment_name(model_name):
    w = WorkspaceClient()
    current_user = w.current_user.me().user_name
    return f"/Users/{current_user}/rag_studio_reviews_{model_name}"


def _check_manage_permissions_for_chain_deployments(model_name, chain_deployments):
    for deployment in chain_deployments:
        _check_manage_permissions_on_deployment(deployment)
    
    if len(chain_deployments) == 0:
        raise ValueError(
            f"The provided {model_name} has never been deployed. "
            "Please deploy the model first using deploy_chain API"
        )


def enable_trace_reviews(
    model_name: str, request_ids: Optional[List[str]] = None
) -> str:
    """
    Enable the reviewer UI to collect feedback on the conversations from the endpoint inference log.

    :param model_name: The name of the UC Registered Model to use when
                registering the chain as a UC Model Version.
                Example: catalog.schema.model_name
    :param request_ids: Optional list of request_ids for which the feedback
                needs to be captured. Example: ["490cf09b-6da6-474f-bc35-ee5ca688ff8d",
                "a4d37810-5cd0-4cbd-aa25-e5ceaf6a448b"]

    :return: URL for the reviewer UI where users can start providing feedback

    Example:
    ```
    from databricks.rag_studio import enable_trace_reviews

    enable_trace_reviews(
        model_name="catalog.schema.chain_model",
        request_ids=["490cf09b-6da6-474f-bc35-ee5ca688ff8", "a4d37810-5cd0-4cbd-aa25-e5ceaf6a448"],
    )
    ```
    """
    chain_deployments = rest_get_chain_deployments(model_name)
    _check_manage_permissions_for_chain_deployments(model_name, chain_deployments)

    chain_deployment = chain_deployments[-1]
    serving_endpoint_name = chain_deployment.endpoint_name
    table_full_name = _get_inference_table_from_serving(
        model_name, serving_endpoint_name
    )

    if request_ids:
        # cast id to int if other type is passed in
        request_ids_str = ", ".join([f"'{id}'" for id in request_ids])
        sql_query = f"SELECT * FROM {table_full_name} WHERE databricks_request_id IN ({request_ids_str})"
    else:
        sql_query = f"SELECT * FROM {table_full_name}"

    from pyspark.sql import SparkSession

    spark = SparkSession.builder.getOrCreate()
    try:
        spark_df = spark.sql(sql_query)
        converted_spark_df, _ = unpack_and_split_payloads(spark_df)
        df = converted_spark_df.toPandas()
    except Exception as e:
        raise ValueError(
            f"Failed to fetch the data from the table {table_full_name}. Error: {str(e)}"
        ) from e

    review_experiment_name = _generate_review_experiment_name(model_name)
    # get or create the review experiment
    review_experiment = mlflow.get_experiment_by_name(review_experiment_name)
    if review_experiment:
        review_experiment_id = review_experiment.experiment_id
    else:
        review_experiment_id = mlflow.create_experiment(review_experiment_name)

    with mlflow.start_run(experiment_id=review_experiment_id) as model_run:
        mlflow.log_table(data=df, artifact_file=_TRACES_FILE_PATH)
        artifact_uri = f"runs:/{model_run.info.run_id}/{_TRACES_FILE_PATH}"
        rest_create_review_artifacts(model_name, artifacts=[artifact_uri])

    return chain_deployment.rag_app_url


def set_review_instructions(model_name: str, instructions: str) -> None:
    """
    Set the instructions for the review UI.

    :param model_name: The name of the UC Registered Model to use when
                registering the chain as a UC Model Version.
                Example: catalog.schema.model_name
    :param instructions: Instructions for the reviewer UI in markdown format

    Example:
    ```
    from databricks.rag_studio import set_review_instructions

    set_review_instructions(
        model_name="catalog.schema.chain_model",
        instructions="Please provide feedback on the conversations based on your knowledge of UC."
    )
    ```
    """
    chain_deployments = rest_get_chain_deployments(model_name)
    _check_manage_permissions_for_chain_deployments(model_name, chain_deployments)

    rest_set_review_instructions(model_name, instructions)


def get_review_instructions(model_name: str) -> str:
    """
    Get the instructions for the review UI.

    :param model_name: The name of the UC Registered Model to use when
                registering the chain as a UC Model Version.
                Example: catalog.schema.model_name

    :return: Instructions for the reviewer UI in markdown format

    Example:
    ```
    from databricks.rag_studio import get_review_instructions

    instructions = get_review_instructions(model_name="catalog.schema.chain_model")
    print(instructions)
    ```
    """
    chain_deployments = rest_get_chain_deployments(model_name)
    _check_manage_permissions_for_chain_deployments(model_name, chain_deployments)

    return rest_get_review_instructions(model_name)
