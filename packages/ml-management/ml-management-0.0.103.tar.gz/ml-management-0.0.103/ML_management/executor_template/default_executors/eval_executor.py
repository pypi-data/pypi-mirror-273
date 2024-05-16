"""Define evaluate executor class."""
from ML_management.executor_template.base_executor import BaseExecutor
from ML_management.executor_template.patterns import OneModelPattern
from ML_management.executor_template.upload_model_mode import UploadModelMode
from ML_management.models.model_type_to_methods_map import ModelMethodName


class EvalExecutor(BaseExecutor):
    """Eval executor from pattern with defined settings parameters."""

    def __init__(self):
        super().__init__(
            executor_name="eval",
            executor_models_pattern=OneModelPattern(
                desired_model_methods=[ModelMethodName.evaluate_function],
                upload_model_modes=UploadModelMode.none,
            ),
        )

    def execute(self):
        """Define execute function that calls evaluate_function of model with corresponding params."""
        self.model.dataset = self.dataset
        return self.model.evaluate_function(**self.model_methods_parameters[ModelMethodName.evaluate_function])
