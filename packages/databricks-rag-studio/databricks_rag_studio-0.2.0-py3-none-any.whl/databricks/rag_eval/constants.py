"""
File containing all the constants needed for the rag utils.
"""

# Metrics
GROUND_TRUTH_RETRIEVAL_METRIC_NAMES = ["precision", "recall"]

# Databricks built-in judge name and endpoint
DATABRICKS_JUDGE_NAME = "databricks_eval"
DATABRICKS_JUDGE_DEFAULT_ENDPOINT = "llmproxy:/gpt-35-turbo-0613-non-interactive"

# EvaluationMetric arguments
METRIC_ARG_KEY__MODEL: str = "model"
METRIC_ARG_KEY__EXAMPLES: str = "examples"
DEFAULT_THRESHOLD_FOR_LLM_JUDGE = 4

# Configs
ALLOWED_CUSTOM_ENDPOINTS_PREFIX = "endpoints"
EVALUATOR_CONFIG_KEY_NAME = "config_yml"
