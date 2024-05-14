from mlflow.models import ModelConfig
from typing import Optional
from mlflow.utils.annotations import deprecated


@deprecated("Use `mlflow.models.ModelConfig` instead")
class RagConfig:
    def __init__(
        self,
        config_path: Optional[str] = None,
        *,
        development_config: Optional[str] = None
    ):
        self.model_config = ModelConfig(
            development_config=development_config or config_path,
        )

    def get(self, key):
        """Delegates the get method to ModelConfig."""
        return self.model_config.get(key)
