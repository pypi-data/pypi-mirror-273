"""Env vars that can be set for the RAG eval."""

# noinspection PyProtectedMember
from mlflow.environment_variables import (
    _BooleanEnvironmentVariable,
    _EnvironmentVariable,
)

# Whether to enable rate limiting for the assessment.
# If set to ``False``, the rate limiter will be disabled for all assessments.
# (default: ``True``)
RAG_EVAL_ENABLE_RATE_LIMIT_FOR_ASSESSMENT = _BooleanEnvironmentVariable(
    "RAG_EVAL_ENABLE_RATE_LIMIT_FOR_ASSESSMENT", True
)

# Rate limit quota for the assessment.
# (default: ``2.0``)
RAG_EVAL_RATE_LIMIT_QUOTA = _EnvironmentVariable(
    "RAG_EVAL_RATE_LIMIT_QUOTA", float, 2.0
)

# Rate limit time_window for the assessment. Unit: seconds.
# (default: ``1.0``)
RAG_EVAL_RATE_LIMIT_TIME_WINDOW_IN_SECONDS = _EnvironmentVariable(
    "RAG_EVAL_RATE_LIMIT_TIME_WINDOW_IN_SECONDS", float, 1.0
)


# Maximum number of workers to run the eval job.
# (default: ``10``)
RAG_EVAL_MAX_WORKERS = _EnvironmentVariable("RAG_EVAL_MAX_WORKERS", int, 10)

# Maximum number of retries when invoking the LLM judge.
# (default: ``60``)
RAG_EVAL_LLM_JUDGE_MAX_RETRIES_ENV_VAR = _EnvironmentVariable("RAG_EVAL_LLM_JUDGE_MAX_RETRIES", int, 60)

# Backoff factor in seconds when invoking the LLM judge. Defaulting to 0 to rely on client side rate limiting to
# maximize throughput
# (default: ``0``)
RAG_EVAL_LLM_JUDGE_BACKOFF_FACTOR_ENV_VAR = _EnvironmentVariable("RAG_EVAL_LLM_JUDGE_BACKOFF_FACTOR", float, 0)

# Jitter in seconds to add to the backoff factor when invoking the LLM judge.
# (default: ``5``)
RAG_EVAL_LLM_JUDGE_BACKOFF_JITTER_ENV_VAR = _EnvironmentVariable("RAG_EVAL_LLM_JUDGE_BACKOFF_JITTER", float, 5)