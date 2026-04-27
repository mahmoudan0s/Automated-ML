from __future__ import annotations

from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder


def create_one_hot_encoder() -> OneHotEncoder:
    # sklearn 1.2+ uses sparse_output, while older versions use sparse.
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


class OrderedLabelEncoder(BaseEstimator, TransformerMixin):
    """Label-like encoder for ordered categorical columns."""

    def __init__(self, category_orders: Optional[Dict[str, List[Any]]] = None) -> None:
        self.category_orders = category_orders or {}
        self._mappings: Dict[str, Dict[Any, int]] = {}
        self._columns: List[str] = []

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> "OrderedLabelEncoder":
        X_df = pd.DataFrame(X).copy()
        self._columns = list(X_df.columns)
        self._mappings = {}

        for col in self._columns:
            if col in self.category_orders and self.category_orders[col]:
                ordered_values = list(self.category_orders[col])
            else:
                ordered_values = list(pd.Series(X_df[col]).dropna().unique())

            self._mappings[col] = {val: idx for idx, val in enumerate(ordered_values)}

        return self

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        X_df = pd.DataFrame(X).copy()
        encoded_columns: List[np.ndarray] = []

        for col in self._columns:
            mapping = self._mappings[col]
            encoded = X_df[col].map(mapping).fillna(-1).astype(float).to_numpy()
            encoded_columns.append(encoded)

        return np.column_stack(encoded_columns) if encoded_columns else np.empty((len(X_df), 0))
