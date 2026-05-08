from __future__ import annotations

from typing import Any, List, Tuple

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler


SCALE_WITH_MINMAX_MODELS = {"svm", "kmeans", "dbscan"}


def detect_outliers(
    df: pd.DataFrame,
    numerical_columns: List[str],
    iqr_factor: float = 1.5,
    outlier_row_ratio_threshold: float = 0.05,
) -> bool:
    if not numerical_columns:
        return False

    numeric_df = df[numerical_columns]
    q1 = numeric_df.quantile(0.25)
    q3 = numeric_df.quantile(0.75)
    iqr = q3 - q1

    lower = q1 - iqr_factor * iqr
    upper = q3 + iqr_factor * iqr

    outlier_mask = (numeric_df.lt(lower)) | (numeric_df.gt(upper))
    outlier_rows = outlier_mask.any(axis=1)
    return float(outlier_rows.mean()) >= outlier_row_ratio_threshold


def choose_scaler(model_name: str, has_outliers: bool) -> Tuple[Any, str]:
    model_key = model_name.lower().strip()

    if has_outliers:
        return RobustScaler(), "RobustScaler"
    if model_key in SCALE_WITH_MINMAX_MODELS:
        return MinMaxScaler(), "MinMaxScaler"
    return StandardScaler(), "StandardScaler"
