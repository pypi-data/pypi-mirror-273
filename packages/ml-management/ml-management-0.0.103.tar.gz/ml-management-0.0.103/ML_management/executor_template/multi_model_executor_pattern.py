"""Executor template for custom executor."""
from typing import Dict, List

from ML_management.executor_template.base_executor import BaseExecutor
from ML_management.executor_template.patterns import ArbitraryModelsPattern
from ML_management.executor_template.upload_model_mode import UploadModelMode
from ML_management.models.model_type_to_methods_map import ModelMethodName


class MultiModelExecutorPattern(BaseExecutor):
    """DEPRECATED.

    Exists only for backward compatibility.
    Instead use BaseExecutor from ML_management.executor_template.base_executor.
    """

    def __init__(
        self,
        executor_name: str,
        desired_model_methods: Dict[str, List[ModelMethodName]],
        upload_model_modes: Dict[str, UploadModelMode],
    ) -> None:
        super().__init__(
            executor_name,
            executor_models_pattern=ArbitraryModelsPattern(
                desired_model_methods=desired_model_methods, upload_model_modes=upload_model_modes
            ),
        )
