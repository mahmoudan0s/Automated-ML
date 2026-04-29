from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

import pandas as pd

from .classification import CLASSIFICATION_MODELS, get_classification_estimator, run_classification_pipeline
from .clustering import CLUSTERING_MODELS, get_clustering_estimator, run_clustering_pipeline
from .regression import REGRESSION_MODELS, get_regression_estimator, run_regression_pipeline
from ..pipeline.full_pipeline import ModelPipelineArtifacts


def get_estimator(model_name: str, random_state: int = 42):
    name = model_name.lower().strip()

    try:
        return get_classification_estimator(name, random_state=random_state)
    except ValueError:
        pass

    try:
        return get_clustering_estimator(name, random_state=random_state)
    except ValueError:
        pass

    try:
        return get_regression_estimator(name, random_state=random_state)
    except ValueError:
        pass

    raise ValueError(
        "Unsupported model_name. Use one of: svm, kmeans, dbscan, random_forest, logistic_regression, linear_regression, random_forest_regressor, svr"
    )


def fit_model_pipeline(
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

    if name in CLASSIFICATION_MODELS:
        return run_classification_pipeline(
            df=df,
            target_column=target_column,
            model_name=name,
            ordered_categorical_features=ordered_categorical_features,
            category_orders=category_orders,
            enable_resampling=enable_resampling,
            resampling_method=resampling_method,
            imbalance_ratio_threshold=imbalance_ratio_threshold,
            correlation_threshold=correlation_threshold,
            random_state=random_state,
        )

    if name in REGRESSION_MODELS:
        return run_regression_pipeline(
            df=df,
            target_column=target_column,
            model_name=name,
            ordered_categorical_features=ordered_categorical_features,
            category_orders=category_orders,
            correlation_threshold=correlation_threshold,
            random_state=random_state,
        )

    if name in CLUSTERING_MODELS:
        return run_clustering_pipeline(
            df=df,
            target_column=target_column,
            model_name=name,
            ordered_categorical_features=ordered_categorical_features,
            category_orders=category_orders,
            correlation_threshold=correlation_threshold,
            random_state=random_state,
        )

    raise ValueError(
        "Unsupported model_name. Use one of: svm, kmeans, dbscan, random_forest, logistic_regression, linear_regression, random_forest_regressor, svr"
    )


def build_model_pipeline(
    df: pd.DataFrame,
    target_column: str,
    model_name: str,
    ordered_categorical_features: Optional[Iterable[str]] = None,
    category_orders: Optional[Dict[str, List[Any]]] = None,
    correlation_threshold: float = 0.6,
    random_state: int = 42,
) -> ModelPipelineArtifacts:
    # For backward compatibility, this now returns a fitted pipeline through the model files.
    return fit_model_pipeline(
        df=df,
        target_column=target_column,
        model_name=model_name,
        ordered_categorical_features=ordered_categorical_features,
        category_orders=category_orders,
        correlation_threshold=correlation_threshold,
        random_state=random_state,
    )


__all__ = [
    "ModelPipelineArtifacts",
    "get_estimator",
    "build_model_pipeline",
    "fit_model_pipeline",
    "run_classification_pipeline",
    "run_regression_pipeline",
    "run_clustering_pipeline",
    "get_classification_estimator",
    "get_clustering_estimator",
    "get_regression_estimator",
]
