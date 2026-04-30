from __future__ import annotations
from typing import Any, Dict

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

def train_classification(X_train, y_train, X_test, y_test) -> Dict[str, Any]:
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
        classifiers[model_name] = SVC(kernel=kernel, random_state=42, **params)

    best_name = None
    best_model = None
    best_accuracy = float("-inf")
    metrics: Dict[str, Dict[str, float]] = {}

    for name, model in classifiers.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        cm = confusion_matrix(y_test, y_pred)

        metrics[name] = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "confusion_matrix": cm.tolist(),
        }

        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_name = name
            best_model = model

    best_metrics = metrics.get(best_name, {})
    return {
        "best_model_name": best_name,
        "best_model": best_model,
        "best_metrics": best_metrics,
        "metrics": metrics,
    }