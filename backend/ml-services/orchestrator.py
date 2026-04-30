from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

from models.regression import train_regression
from preprocessing.preprocessing import (
    encode_target_labels,
    impute_missing_values,
    is_target_imbalanced,
    one_hot_encode_categorical,
    random_oversample,
    scale_numeric_features,
)

def preprocess(
    df: pd.DataFrame,
    target: Optional[str],
    task: str,
) -> Tuple[Any, Any, Dict[str, Any]]:
    supervised_tasks = {"classification", "regression"}
    if task in supervised_tasks:
        if not target or target not in df.columns:
            raise ValueError("target column is required and must exist in the dataset")
        y = df[target]
        X = df.drop(columns=[target])
    else:
        y = None
        X = df.copy()

    preprocessor = Pipeline(
        steps=[
            ("impute", FunctionTransformer(impute_missing_values, validate=False)),
            ("encode", FunctionTransformer(one_hot_encode_categorical, validate=False)),
            ("scale", FunctionTransformer(scale_numeric_features, validate=False)),
        ]
    )

    X = preprocessor.fit_transform(X)
    if y is not None and hasattr(X, "index"):
        y = y.loc[X.index]

    if len(X) == 0:
        raise ValueError("All rows were dropped during preprocessing. Adjust missing-value thresholds.")

    artifacts: Dict[str, Any] = {}
    if task == "classification" and y is not None:
        y, label_encoder = encode_target_labels(y)
        artifacts["label_encoder"] = label_encoder

        if is_target_imbalanced(y):
            X_resampled, y_resampled = random_oversample(X.to_numpy(), y.to_numpy())
            return X_resampled, y_resampled, artifacts

    return X, y, {"preprocessor": preprocessor, **artifacts}


def run_pipeline(df, task, target=None):

    # 1. preprocessing
    X, y, preprocessor = preprocess(df, target, task)

    # 2. split (supervised)
    if task in ["classification", "regression"]:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

    # 3. training + evaluation
    if task == "regression":
        result = train_regression(X_train, y_train, X_test, y_test)
        return {
            "model": result["best_model"],
            "model_name": result["best_model_name"],
            "metrics": result["best_metrics"],
            "all_metrics": result["metrics"],
            "preprocessor": preprocessor,
        }

    raise ValueError("Invalid task type")