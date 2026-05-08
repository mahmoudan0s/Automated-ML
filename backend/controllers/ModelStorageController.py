from __future__ import annotations

import joblib
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import json


class ModelStorageController:
    """Handle serialization and storage of trained models."""

    def __init__(self):
        self.models_dir = Path(__file__).resolve().parent.parent / "assets" / "models"
        self.models_dir.mkdir(parents=True, exist_ok=True)

    def save_model(
        self,
        model: Any,
        preprocessor: Any,
        model_name: str,
        problem_type: str,
        metadata: Dict[str, Any] = None,
    ) -> str:
        """
        Save trained model and preprocessing pipeline.

        Args:
            model: Trained model object
            preprocessor: Preprocessing pipeline
            model_name: Name of the model algorithm
            problem_type: Type of problem (classification, regression, clustering)
            metadata: Additional metadata to store

        Returns:
            model_id: Unique identifier for the saved model
        """
        # Generate unique model ID using timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_id = f"{problem_type}_{model_name}_{timestamp}"

        model_dir = self.models_dir / model_id
        model_dir.mkdir(parents=True, exist_ok=True)

        # Save model
        model_path = model_dir / "model.joblib"
        joblib.dump(model, model_path)

        # Save preprocessor
        preprocessor_path = model_dir / "preprocessor.joblib"
        joblib.dump(preprocessor, preprocessor_path)

        # Save metadata
        meta = {
            "model_id": model_id,
            "model_name": model_name,
            "problem_type": problem_type,
            "created_at": datetime.now().isoformat(),
            **(metadata or {}),
        }
        metadata_path = model_dir / "metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(meta, f, indent=2)

        return model_id

    def load_model(self, model_id: str) -> Dict[str, Any]:
        """
        Load model and preprocessor from storage.

        Args:
            model_id: Unique identifier of the model

        Returns:
            Dictionary containing model, preprocessor, and metadata
        """
        model_dir = self.models_dir / model_id

        if not model_dir.exists():
            raise FileNotFoundError(f"Model with ID '{model_id}' not found")

        model_path = model_dir / "model.joblib"
        preprocessor_path = model_dir / "preprocessor.joblib"
        metadata_path = model_dir / "metadata.json"

        if not model_path.exists() or not preprocessor_path.exists():
            raise FileNotFoundError(f"Model files for ID '{model_id}' are incomplete")

        model = joblib.load(model_path)
        preprocessor = joblib.load(preprocessor_path)

        metadata = {}
        if metadata_path.exists():
            with open(metadata_path, "r") as f:
                metadata = json.load(f)

        return {
            "model": model,
            "preprocessor": preprocessor,
            "metadata": metadata,
            "model_path": str(model_path),
            "preprocessor_path": str(preprocessor_path),
        }

    def delete_model(self, model_id: str) -> bool:
        """Delete a saved model."""
        model_dir = self.models_dir / model_id

        if not model_dir.exists():
            raise FileNotFoundError(f"Model with ID '{model_id}' not found")

        import shutil
        shutil.rmtree(model_dir)
        return True

    def list_models(self) -> list[Dict[str, Any]]:
        """List all saved models with their metadata."""
        models = []

        if not self.models_dir.exists():
            return models

        for model_dir in self.models_dir.iterdir():
            if not model_dir.is_dir():
                continue

            metadata_path = model_dir / "metadata.json"
            if metadata_path.exists():
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                    models.append(metadata)

        return sorted(models, key=lambda x: x.get("created_at", ""), reverse=True)
