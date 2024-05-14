from typing import List

import requests
from requests import HTTPError

from databricks.rag_eval import env_vars
from databricks.rag_eval.clients.databricks_api_client import DatabricksAPIClient
from databricks.rag_eval.clients.llmjudge import proto_serde
from databricks.rag_eval.config import example_config
from databricks.rag_eval.config.assessment_config import (
    AssessmentType,
)
from databricks.rag_eval.evaluation import entities


class LlmJudgeClient(DatabricksAPIClient):
    """
    Client to interact with the LLM judge service (/chat-assessments).
    """

    def __init__(self, api_url: str, api_token: str):
        super().__init__(
            api_url=api_url,
            api_token=api_token,
            version="2.0",
        )
        self.proto_serde = proto_serde.ChatAssessmentProtoSerde()
        self.max_retries = env_vars.RAG_EVAL_LLM_JUDGE_MAX_RETRIES_ENV_VAR.get()
        self.backoff_factor = env_vars.RAG_EVAL_LLM_JUDGE_BACKOFF_FACTOR_ENV_VAR.get()
        self.backoff_jitter = env_vars.RAG_EVAL_LLM_JUDGE_BACKOFF_JITTER_ENV_VAR.get()

    def get_assessment(
        self,
        eval_item: entities.EvalItem,
        assessment_name: str,
        assessment_type: AssessmentType,
        examples: List[example_config.AssessmentExample],
    ) -> List[entities.AssessmentResult]:
        """
        Retrieves the assessment results from the LLM judge service for the given eval item and requested assessment
        """
        request_json = self.proto_serde.construct_assessment_request_json(
            eval_item, assessment_name, examples
        )

        with self.get_request_session(
            max_retries=self.max_retries,
            backoff_factor=self.backoff_factor,
            backoff_jitter=self.backoff_jitter,
        ) as session:
            resp = session.post(
                self.get_method_url("/rag-studio/chat-assessments"),
                json=request_json,
                auth=self.get_auth(),
            )

        if resp.status_code == requests.codes.ok:
            return self.proto_serde.construct_assessment_result(
                resp.json(), assessment_name
            )
        else:
            try:
                resp.raise_for_status()
            except HTTPError as e:
                return self.proto_serde.construct_assessment_error_result(
                    assessment_name,
                    assessment_type,
                    resp.status_code,
                    e,
                )
