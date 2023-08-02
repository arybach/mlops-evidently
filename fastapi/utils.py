from typing import Callable, Optional, Text
import joblib
import os

class ModelLoader:
    """Model loader singleton."""

    def __init__(self, model_name: str, model_path: Text = 'models'):
        self.model_name: str = model_name
        self.model_path: Text = model_path
        self.model: Optional[Callable] = None

    def get_model(self) -> Callable:
        if self.model is None:  # Check if the model is not loaded
            self._load_model()

        return self.model

    def _load_model(self) -> None:
        model_file_path = os.path.join(self.model_path, f"{self.model_name}.joblib")

        if not os.path.exists(model_file_path):
            raise ValueError(f"Model '{self.model_name}' not found at {model_file_path}")

        self.model = joblib.load(model_file_path)  # Cache the loaded model
