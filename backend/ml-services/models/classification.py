from __future__ import annotations

from typing import Any, Dict

import numpy as np

from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC

def _build_classification_report(y_true, y_pred) -> list[dict[str, Any]]:
    labels = np.unique(y_true)
    precision_values, recall_values, f1_values, support_values = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, zero_division=0
    )

    class_report: list[dict[str, Any]] = []
    for label, precision, recall, f1, support in zip(
        labels, precision_values, recall_values, f1_values, support_values
    ):
        class_report.append(
            {
                "class": int(label) if np.issubdtype(type(label), np.integer) else str(label),
                "precision": round(float(precision), 3),
                "recall": round(float(recall), 3),
                "f1_score": round(float(f1), 3),
                "support": int(support),
            }
        )

    total_support = int(support_values.sum())
    class_report.append(
        {
            "class": "Accuracy",
            "precision": None,
            "recall": None,
            "f1_score": round(float(accuracy_score(y_true, y_pred)), 3),
            "support": total_support,
        }
    )
    class_report.append(
        {
            "class": "Macro Avg",
            "precision": round(float(precision_values.mean()), 3),
            "recall": round(float(recall_values.mean()), 3),
            "f1_score": round(float(f1_values.mean()), 3),
            "support": total_support,
        }
    )

    weighted_precision = float((precision_values * support_values).sum() / total_support) if total_support > 0 else 0.0
    weighted_recall = float((recall_values * support_values).sum() / total_support) if total_support > 0 else 0.0
    weighted_f1 = float((f1_values * support_values).sum() / total_support) if total_support > 0 else 0.0

    class_report.append(
        {
            "class": "Weighted Avg",
            "precision": round(weighted_precision, 3),
            "recall": round(weighted_recall, 3),
            "f1_score": round(weighted_f1, 3),
            "support": total_support,
        }
    )
    return class_report


def _evaluate_classification_model(model, X, y, n_splits: int) -> tuple[dict[str, Any], np.ndarray, float]:
    X_array = X.to_numpy() if hasattr(X, "to_numpy") else np.asarray(X)
    y_array = np.asarray(y)
    splitter = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

    fold_accuracies: list[float] = []
    fold_precisions: list[float] = []
    fold_recalls: list[float] = []
    fold_f1s: list[float] = []
    oof_predictions = np.empty_like(y_array)

    for train_idx, test_idx in splitter.split(X_array, y_array):
        estimator = clone(model)
        X_train_fold = X_array[train_idx]
        y_train_fold = y_array[train_idx]

        estimator.fit(X_train_fold, y_train_fold)
        y_pred = estimator.predict(X_array[test_idx])
        oof_predictions[test_idx] = y_pred

        fold_accuracies.append(accuracy_score(y_array[test_idx], y_pred))
        fold_precisions.append(precision_score(y_array[test_idx], y_pred, average="weighted", zero_division=0))
        fold_recalls.append(recall_score(y_array[test_idx], y_pred, average="weighted", zero_division=0))
        fold_f1s.append(f1_score(y_array[test_idx], y_pred, average="weighted", zero_division=0))

    metrics = {
        "accuracy": float(np.mean(fold_accuracies)) if fold_accuracies else None,
        "accuracy_std": float(np.std(fold_accuracies)) if fold_accuracies else None,
        "precision": float(np.mean(fold_precisions)) if fold_precisions else None,
        "recall": float(np.mean(fold_recalls)) if fold_recalls else None,
        "f1": float(np.mean(fold_f1s)) if fold_f1s else None,
        "fold_accuracies": [round(float(score), 4) for score in fold_accuracies],
    }
    return metrics, oof_predictions, float(np.mean(fold_accuracies)) if fold_accuracies else float("-inf")


def train_classification(X, y) -> Dict[str, Any]:
    classifiers = {
        "logistic_regression": LogisticRegression(max_iter=1000, random_state=42),
        "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
    }

    svm_configs = [
        ("linear", {"C": 0.5}),
        ("linear", {"C": 1.0}),
        ("linear", {"C": 2.0}),
        ("rbf", {"C": 1.0, "gamma": "scale"}),
        ("rbf", {"C": 2.0, "gamma": "scale"}),
        ("rbf", {"C": 1.0, "gamma": 0.1}),
        ("poly", {"C": 1.0, "degree": 2, "gamma": "scale", "coef0": 0.0}),
        ("poly", {"C": 1.0, "degree": 3, "gamma": "scale", "coef0": 1.0}),
        ("poly", {"C": 2.0, "degree": 3, "gamma": "scale", "coef0": 0.0}),
    ]

    for idx, (kernel, params) in enumerate(svm_configs, start=1):
        model_name = f"svm_{idx}_{kernel}"
        classifiers[model_name] = SVC(kernel=kernel, random_state=42, probability=True, **params)

    y_array = np.asarray(y)
    class_counts = np.unique(y_array, return_counts=True)[1]
    n_splits = int(min(5, class_counts.min())) if len(class_counts) else 0
    if n_splits < 2:
        raise ValueError("Classification cross validation requires at least 2 samples per class")

    best_name = None
    best_model = None
    best_accuracy = float("-inf")
    best_oof_predictions = None
    metrics: Dict[str, Dict[str, Any]] = {}
    oof_predictions_per_model: Dict[str, np.ndarray] = {}

    for name, model in classifiers.items():
        cv_metrics, oof_predictions, mean_accuracy = _evaluate_classification_model(model, X, y, n_splits)
        metrics[name] = cv_metrics
        oof_predictions_per_model[name] = oof_predictions

        if mean_accuracy > best_accuracy:
            best_accuracy = mean_accuracy
            best_name = name
            best_model = clone(model)
            best_oof_predictions = oof_predictions

    if best_model is not None:
        best_model.fit(X, np.asarray(y))

    best_metrics = metrics.get(best_name, {})
    if best_oof_predictions is not None:
        best_metrics = {
            **best_metrics,
            "confusion_matrix": confusion_matrix(y_array, best_oof_predictions).tolist(),
            "classification_report": _build_classification_report(y_array, best_oof_predictions),
        }

    # Add confusion_matrix and classification_report to all metrics
    for model_name, oof_preds in oof_predictions_per_model.items():
        metrics[model_name]["confusion_matrix"] = confusion_matrix(y_array, oof_preds).tolist()
        metrics[model_name]["classification_report"] = _build_classification_report(y_array, oof_preds)

    return {
        "best_model_name": best_name,
        "best_model": best_model,
        "best_metrics": best_metrics,
        "metrics": metrics,
    }