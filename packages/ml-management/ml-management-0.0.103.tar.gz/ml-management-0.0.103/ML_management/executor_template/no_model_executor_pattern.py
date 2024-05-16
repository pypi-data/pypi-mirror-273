"""Executor template for custom executor."""

from ML_management.executor_template.base_executor import BaseExecutor
from ML_management.executor_template.patterns import ArbitraryModelsPattern


class NoModelExecutorPattern(BaseExecutor):
    """DEPRECATED.

    Exists only for backward compatibility.
    Instead use BaseExecutor from ML_management.executor_template.base_executor.
    """

    def __init__(self, executor_name: str) -> None:
        super().__init__(
            executor_name,
            executor_models_pattern=ArbitraryModelsPattern(desired_model_methods={}, upload_model_modes={}),
        )
