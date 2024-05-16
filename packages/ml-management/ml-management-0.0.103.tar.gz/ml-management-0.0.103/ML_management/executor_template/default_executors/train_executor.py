"""Define train executor class."""
from ML_management.executor_template.base_executor import BaseExecutor
from ML_management.executor_template.patterns import OneModelPattern
from ML_management.executor_template.upload_model_mode import UploadModelMode
from ML_management.models.model_type_to_methods_map import ModelMethodName


class TrainExecutor(BaseExecutor):
    """Train executor from pattern with defined settings parameters."""

    def __init__(self):
        super().__init__(
            executor_name="train",
            executor_models_pattern=OneModelPattern(
                desired_model_methods=[ModelMethodName.train_function],
                upload_model_modes=UploadModelMode.new_model,
            ),
        )

    def execute(self):
        """Define execute function that calls train_function of model with corresponding params."""
        self.model.dataset = self.dataset
        return self.model.train_function(**self.model_methods_parameters[ModelMethodName.train_function])
