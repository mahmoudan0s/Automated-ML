from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from .encoding import OrderedLabelEncoder, create_one_hot_encoder
from .missing_values import get_categorical_imputer, get_numeric_imputer
from .scaling import choose_scaler, detect_outliers


@dataclass
class PreprocessingArtifacts:
    preprocessor: ColumnTransformer
    numerical_features: List[str]
    ordered_categorical_features: List[str]
    unordered_categorical_features: List[str]
    imputation_strategy: str
    scaler_used: str


def _build_preprocessor(
    df: pd.DataFrame,
    target_column: str,
    model_name: str,
    ordered_categorical_features: Optional[Iterable[str]] = None,
    category_orders: Optional[Dict[str, List[Any]]] = None,
    correlation_threshold: float = 0.6,
) -> Tuple[ColumnTransformer, Dict[str, Any]]:
    features_df = df.drop(columns=[target_column])

    numerical_features = features_df.select_dtypes(include=["number"]).columns.tolist()
    categorical_features = features_df.select_dtypes(exclude=["number"]).columns.tolist()

    ordered_set = set(ordered_categorical_features or [])
    ordered_cat = [col for col in categorical_features if col in ordered_set]
    unordered_cat = [col for col in categorical_features if col not in ordered_set]

    num_imputer, imputation_strategy = get_numeric_imputer(
        df=df,
        numerical_columns=numerical_features,
        correlation_threshold=correlation_threshold,
    )

    has_outliers_flag = detect_outliers(df, numerical_features)
    scaler, scaler_name = choose_scaler(model_name=model_name, has_outliers=has_outliers_flag)

    transformers = []

    if numerical_features:
        numeric_pipeline = Pipeline(
            steps=[
                ("imputer", num_imputer),
                ("scaler", scaler),
            ]
        )
        transformers.append(("num", numeric_pipeline, numerical_features))

    if ordered_cat:
        ordered_pipeline = Pipeline(
            steps=[
                ("imputer", get_categorical_imputer()),
                ("encoder", OrderedLabelEncoder(category_orders=category_orders)),
            ]
        )
        transformers.append(("ordered_cat", ordered_pipeline, ordered_cat))

    if unordered_cat:
        unordered_pipeline = Pipeline(
            steps=[
                ("imputer", get_categorical_imputer()),
                ("encoder", create_one_hot_encoder()),
            ]
        )
        transformers.append(("unordered_cat", unordered_pipeline, unordered_cat))

    preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")

    metadata = {
        "numerical_features": numerical_features,
        "ordered_categorical_features": ordered_cat,
        "unordered_categorical_features": unordered_cat,
        "imputation_strategy": imputation_strategy,
        "scaler_used": scaler_name,
    }

    return preprocessor, metadata


def build_preprocessor(
    df: pd.DataFrame,
    target_column: str,
    model_name: str,
    ordered_categorical_features: Optional[Iterable[str]] = None,
    category_orders: Optional[Dict[str, List[Any]]] = None,
    correlation_threshold: float = 0.6,
    ) -> PreprocessingArtifacts:
    if target_column not in df.columns:
        raise ValueError(f"target_column '{target_column}' was not found in the dataframe")

    preprocessor, metadata = _build_preprocessor(
        df=df,
        target_column=target_column,
        model_name=model_name,
        ordered_categorical_features=ordered_categorical_features,
        category_orders=category_orders,
        correlation_threshold=correlation_threshold,
    )

    return PreprocessingArtifacts(
        preprocessor=preprocessor,
        numerical_features=metadata["numerical_features"],
        ordered_categorical_features=metadata["ordered_categorical_features"],
        unordered_categorical_features=metadata["unordered_categorical_features"],
        imputation_strategy=metadata["imputation_strategy"],
        scaler_used=metadata["scaler_used"],
    )


def split_features_target(df: pd.DataFrame, target_column: str) -> Tuple[pd.DataFrame, pd.Series]:
    if target_column not in df.columns:
        raise ValueError(f"target_column '{target_column}' was not found in the dataframe")
    return df.drop(columns=[target_column]), df[target_column]


__all__ = [
    "PreprocessingArtifacts",
    "build_preprocessor",
    "split_features_target",
    "OrderedLabelEncoder",
    "create_one_hot_encoder",
    "get_numeric_imputer",
    "get_categorical_imputer",
    "choose_scaler",
    "detect_outliers",
]
