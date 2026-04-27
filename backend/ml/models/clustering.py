from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

import pandas as pd

from sklearn.cluster import DBSCAN, KMeans

from ..pipeline.full_pipeline import ModelPipelineArtifacts, fit_pipeline_with_estimator


CLUSTERING_MODELS = {"kmeans", "dbscan"}


def get_clustering_estimator(model_name: str, random_state: int = 42):
    name = model_name.lower().strip()

    if name == "kmeans":
        return KMeans(n_clusters=3, random_state=random_state, n_init=10)
    if name == "dbscan":
        return DBSCAN(eps=0.5, min_samples=5)

    raise ValueError("Unsupported clustering model_name. Use: kmeans, dbscan")


def run_clustering_pipeline(
    df: pd.DataFrame,
    target_column: str,
    model_name: str,
    ordered_categorical_features: Optional[Iterable[str]] = None,
    category_orders: Optional[Dict[str, List[Any]]] = None,
    correlation_threshold: float = 0.6,
    random_state: int = 42,
) -> ModelPipelineArtifacts:
    name = model_name.lower().strip()
    if name not in CLUSTERING_MODELS:
        raise ValueError("model_name is not a supported clustering model")

    estimator = get_clustering_estimator(name, random_state=random_state)
    # Resampling is not applicable for clustering tasks.
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
