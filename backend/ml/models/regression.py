from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR

from ..pipeline.full_pipeline import ModelPipelineArtifacts, fit_pipeline_with_estimator


REGRESSION_MODELS = {"linear_regression", "random_forest_regressor", "svr"}


def get_regression_estimator(model_name: str, random_state: int = 42):
    name = model_name.lower().strip()

    if name == "linear_regression":
        return LinearRegression()
    if name == "random_forest_regressor":
        return RandomForestRegressor(n_estimators=300, random_state=random_state)
    if name == "svr":
        return SVR()

    raise ValueError("Unsupported regression model_name. Use: linear_regression, random_forest_regressor, svr")


def run_regression_pipeline(
    df: pd.DataFrame,
    target_column: str,
    model_name: str,
    ordered_categorical_features: Optional[Iterable[str]] = None,
    category_orders: Optional[Dict[str, List[Any]]] = None,
    correlation_threshold: float = 0.6,
    random_state: int = 42,
) -> ModelPipelineArtifacts:
    name = model_name.lower().strip()
    if name not in REGRESSION_MODELS:
        raise ValueError("model_name is not a supported regression model")

    estimator = get_regression_estimator(name, random_state=random_state)
    # Resampling is a classification technique, so it is disabled for regression.
    return fit_pipeline_with_estimator(
        df=df,
        target_column=target_column,
        model_name=name,
        estimator=estimator,
        ordered_categorical_features=ordered_categorical_features,
        category_orders=category_orders,
        enable_resampling=False,
        correlation_threshold=correlation_threshold,
        random_state=random_state,
    )
