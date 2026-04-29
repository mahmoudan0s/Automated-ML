from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from ..pipeline.full_pipeline import ModelPipelineArtifacts, fit_pipeline_with_estimator


CLASSIFICATION_MODELS = {"svm", "random_forest", "logistic_regression"}


def get_classification_estimator(model_name: str, random_state: int = 42):
    name = model_name.lower().strip()

    if name == "svm":
        return SVC(probability=True, random_state=random_state)
    if name == "random_forest":
        return RandomForestClassifier(n_estimators=300, random_state=random_state)
    if name == "logistic_regression":
        return LogisticRegression(max_iter=1000, random_state=random_state)

    raise ValueError("Unsupported classification model_name. Use: svm, random_forest, logistic_regression")


def run_classification_pipeline(
    df: pd.DataFrame,
    target_column: str,
    model_name: str,
    ordered_categorical_features: Optional[Iterable[str]] = None,
    category_orders: Optional[Dict[str, List[Any]]] = None,
    enable_resampling: bool = True,
    resampling_method: str = "random",
    imbalance_ratio_threshold: float = 0.67,
    correlation_threshold: float = 0.6,
    random_state: int = 42,
) -> ModelPipelineArtifacts:
    name = model_name.lower().strip()
    if name not in CLASSIFICATION_MODELS:
        raise ValueError("model_name is not a supported classification model")

    estimator = get_classification_estimator(name, random_state=random_state)
    return fit_pipeline_with_estimator(
        df=df,
        target_column=target_column,
        model_name=name,
        estimator=estimator,
        ordered_categorical_features=ordered_categorical_features,
        category_orders=category_orders,
        enable_resampling=enable_resampling,
        resampling_method=resampling_method,
        imbalance_ratio_threshold=imbalance_ratio_threshold,
        correlation_threshold=correlation_threshold,
        random_state=random_state,
    )
