from __future__ import annotations
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer, SimpleImputer


def has_correlated_features(
    df: pd.DataFrame,
    numerical_columns: List[str],
    correlation_threshold: float = 0.6,
) -> bool:
    if len(numerical_columns) < 2:
        return False

    corr_matrix = df[numerical_columns].corr(numeric_only=True).abs()
    if corr_matrix.empty:
        return False

    mask = np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    upper_tri = corr_matrix.where(mask)
    return bool((upper_tri > correlation_threshold).any().any())


def get_numeric_imputer(
    df: pd.DataFrame,
    numerical_columns: List[str],
    correlation_threshold: float = 0.6,
) -> Tuple[object, str]:
    if has_correlated_features(df, numerical_columns, correlation_threshold=correlation_threshold):
        return KNNImputer(n_neighbors=5), "KNNImputer"
    return SimpleImputer(strategy="median"), "Median(SimpleImputer)"


def get_categorical_imputer() -> SimpleImputer:
    return SimpleImputer(strategy="most_frequent")
