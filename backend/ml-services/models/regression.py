from __future__ import annotations

from typing import Any, Dict

import numpy as np

from sklearn.base import clone
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold


def _evaluate_regression_model(model, X, y, n_splits: int) -> tuple[dict[str, Any], np.ndarray, float]:
    X_array = X.to_numpy() if hasattr(X, "to_numpy") else np.asarray(X)
    y_array = np.asarray(y)
    splitter = KFold(n_splits=n_splits, shuffle=True, random_state=42)

    fold_r2_scores: list[float] = []
    fold_mae_scores: list[float] = []
    fold_mse_scores: list[float] = []
    oof_predictions = np.empty_like(y_array, dtype=float)

    for train_idx, test_idx in splitter.split(X_array):
        estimator = clone(model)
        estimator.fit(X_array[train_idx], y_array[train_idx])
        y_pred = estimator.predict(X_array[test_idx])
        oof_predictions[test_idx] = y_pred

        fold_mae_scores.append(mean_absolute_error(y_array[test_idx], y_pred))
        fold_mse_scores.append(mean_squared_error(y_array[test_idx], y_pred))
        fold_r2_scores.append(r2_score(y_array[test_idx], y_pred))

    mean_r2 = float(np.mean(fold_r2_scores)) if fold_r2_scores else float("nan")
    metrics = {
        "accuracy": mean_r2,
        "mae": float(np.mean(fold_mae_scores)) if fold_mae_scores else None,
        "mse": float(np.mean(fold_mse_scores)) if fold_mse_scores else None,
        "r2": mean_r2,
        "r2_std": float(np.std(fold_r2_scores)) if fold_r2_scores else None,
        "fold_r2_scores": [round(float(score), 4) for score in fold_r2_scores],
    }
    return metrics, oof_predictions, mean_r2


def train_regression(X, y) -> Dict[str, Any]:
    regressors = {
        "linear": LinearRegression(),
        "random_forest": RandomForestRegressor(n_estimators=100, random_state=42),
    }

    ridge_alphas = [0.01, 0.1, 1.0, 10.0, 100.0]
    for alpha in ridge_alphas:
        regressors[f"ridge_alpha_{alpha}"] = Ridge(alpha=alpha, random_state=42)

    n_splits = min(5, len(X))
    if n_splits < 2:
        raise ValueError("Regression cross validation requires at least 2 rows")

    best_name = None
    best_model = None
    best_r2 = float("-inf")
    best_oof_predictions = None
    metrics: Dict[str, Dict[str, Any]] = {}

    for name, model in regressors.items():
        cv_metrics, oof_predictions, mean_r2 = _evaluate_regression_model(model, X, y, n_splits)
        metrics[name] = cv_metrics

        if mean_r2 > best_r2:
            best_r2 = mean_r2
            best_name = name
            best_model = clone(model)
            best_oof_predictions = oof_predictions

    if best_model is not None:
        # Fit on the original DataFrame (not a numpy array) so the model
        # stores feature names — prevents the sklearn UserWarning when
        # permutation_importance or other inspectors pass a DataFrame later.
        best_model.fit(X, y)

    best_metrics = metrics.get(best_name, {})
    if best_oof_predictions is not None:
        y_array = np.asarray(y)
        best_metrics = {
            **best_metrics,
            "mae": float(mean_absolute_error(y_array, best_oof_predictions)),
            "mse": float(mean_squared_error(y_array, best_oof_predictions)),
            "r2": float(r2_score(y_array, best_oof_predictions)),
        }

    return {
        "best_model_name": best_name,
        "best_model": best_model,
        "best_metrics": best_metrics,
        "metrics": metrics,
    }
