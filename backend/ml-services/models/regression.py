from __future__ import annotations

from typing import Any, Dict

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def train_regression(X_train, y_train, X_test, y_test) -> Dict[str, Any]:
    regressor = {
        "linear": LinearRegression(),
        "random_forest": RandomForestRegressor(n_estimators=100, random_state=42),
    }

    ridge_alphas = [0.01, 0.1, 1.0, 10.0, 100.0]
    for alpha in ridge_alphas:
        regressor[f"ridge_alpha_{alpha}"] = Ridge(alpha=alpha, random_state=42)

    best_name = None
    best_model = None
    best_r2 = float("-inf")
    metrics: Dict[str, Dict[str, float]] = {}

    for name, model in regressor.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        metrics[name] = {
            "accuracy": r2,
            "mae": mae,
            "mse": mse,
            "r2": r2,
        }

        if r2 > best_r2:
            best_r2 = r2
            best_name = name
            best_model = model

    best_metrics = metrics.get(best_name, {})
    return {
        "best_model_name": best_name,
        "best_model": best_model,
        "best_metrics": best_metrics,
        "metrics": metrics,
    }
