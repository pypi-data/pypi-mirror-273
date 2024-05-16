"""Executor template for custom executor."""
from typing import List

from ML_management.executor_template.base_executor import BaseExecutor
from ML_management.executor_template.patterns import OneModelPattern
from ML_management.executor_template.upload_model_mode import UploadModelMode
from ML_management.models.model_type_to_methods_map import ModelMethodName


class JobExecutorPattern(BaseExecutor):
    """DEPRECATED.

    Exists only for backward compatibility.
    Instead use BaseExecutor from ML_management.executor_template.base_executor.
    """

    def __init__(
        self, executor_name: str, desired_model_methods: List[ModelMethodName], upload_model_mode: UploadModelMode
    ) -> None:
        super().__init__(
            executor_name,
            executor_models_pattern=OneModelPattern(
                upload_model_modes=upload_model_mode, desired_model_methods=desired_model_methods
            ),
        )
