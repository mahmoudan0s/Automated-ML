from __future__ import annotations

from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering, DBSCAN, KMeans
from sklearn.metrics import silhouette_score


def _choose_k_by_silhouette(
	X: np.ndarray,
	k_min: int = 2,
	k_max: int = 10,
) -> Tuple[int | None, float | None]:
	n_samples = X.shape[0]
	if n_samples < 3:
		return None, None

	max_k = min(k_max, n_samples - 1)
	if max_k < k_min:
		return None, None

	best_k = None
	best_score = float("-inf")

	for k in range(k_min, max_k + 1):
		model = KMeans(n_clusters=k, random_state=42, n_init=10)
		labels = model.fit_predict(X)
		if len(set(labels)) < 2:
			continue
		score = silhouette_score(X, labels)
		if score > best_score:
			best_score = score
			best_k = k

	if best_k is None:
		return None, None

	return best_k, best_score


def _summarize_clusters(X_df: pd.DataFrame, labels: np.ndarray) -> Dict[str, str]:
	numeric_df = X_df.select_dtypes(include=["number"]).copy()
	if numeric_df.empty:
		return {}

	overall_means = numeric_df.mean()
	overall_medians = numeric_df.median()
	summaries: Dict[str, str] = {}
	total_rows = len(numeric_df)

	for label in np.unique(labels):
		if label == -1:
			noise_count = int((labels == -1).sum())
			summaries["noise"] = (
				f"Noise points that do not belong to any cluster ({noise_count} rows)."
			)
			continue

		cluster_df = numeric_df[labels == label]
		if cluster_df.empty:
			summaries[str(label)] = "Cluster is empty."
			continue

		cluster_size = len(cluster_df)
		cluster_share = (cluster_size / total_rows) * 100 if total_rows else 0.0
		cluster_means = cluster_df.mean()
		diff = cluster_means - overall_means
		top_high = diff.sort_values(ascending=False).head(3)
		top_low = diff.sort_values(ascending=True).head(3)

		high_parts = []
		for feature, delta in top_high.items():
			mean_value = cluster_means[feature]
			overall_value = overall_means[feature]
			median_value = overall_medians[feature]
			if pd.isna(delta):
				continue
			high_parts.append(
				f"{feature} ({mean_value:.3f} vs overall {overall_value:.3f}, median {median_value:.3f})"
			)

		low_parts = []
		for feature, delta in top_low.items():
			mean_value = cluster_means[feature]
			overall_value = overall_means[feature]
			median_value = overall_medians[feature]
			if pd.isna(delta):
				continue
			low_parts.append(
				f"{feature} ({mean_value:.3f} vs overall {overall_value:.3f}, median {median_value:.3f})"
			)

		summaries[str(label)] = (
			f"Cluster {label} contains {cluster_size} rows ({cluster_share:.1f}% of the data). "
			f"Compared with the overall dataset, it is strongest in: {', '.join(high_parts) if high_parts else 'no clear numeric uplift'}. "
			f"It is weakest in: {', '.join(low_parts) if low_parts else 'no clear numeric drop'}. "
			f"This means the cluster represents a group whose numeric profile differs from the average on the features above."
		)

	return summaries


def train_clustering(X: pd.DataFrame) -> Dict[str, Any]:
	X_df = X.copy()
	X_array = X_df.to_numpy()

	metrics: Dict[str, Dict[str, Any]] = {}
	best_name = None
	best_model = None
	best_score = float("-inf")
	best_labels: np.ndarray | None = None

	k_best, k_score = _choose_k_by_silhouette(X_array, k_min=2, k_max=10)
	if k_best is not None:
		kmeans = KMeans(n_clusters=k_best, random_state=42, n_init=10)
		labels = kmeans.fit_predict(X_array)
		score = silhouette_score(X_array, labels)
		metrics["kmeans"] = {
			"silhouette": score,
			"n_clusters": k_best,
		}
		if score > best_score:
			best_score = score
			best_name = "kmeans"
			best_model = kmeans
			best_labels = labels

	if k_best is not None:
		agglom = AgglomerativeClustering(n_clusters=k_best)
		labels = agglom.fit_predict(X_array)
		if len(set(labels)) > 1:
			score = silhouette_score(X_array, labels)
			metrics["agglomerative"] = {
				"silhouette": score,
				"n_clusters": k_best,
			}
			if score > best_score:
				best_score = score
				best_name = "agglomerative"
				best_model = agglom
				best_labels = labels

	dbscan = DBSCAN(eps=0.5, min_samples=5)
	dbscan_labels = dbscan.fit_predict(X_array)
	unique_labels = set(dbscan_labels)
	n_clusters = len([lbl for lbl in unique_labels if lbl != -1])
	if n_clusters >= 2:
		score = silhouette_score(X_array, dbscan_labels)
	else:
		score = float("-inf")

	metrics["dbscan"] = {
		"silhouette": score if score != float("-inf") else None,
		"n_clusters": n_clusters,
		"noise_points": int((dbscan_labels == -1).sum()),
	}

	if score > best_score:
		best_score = score
		best_name = "dbscan"
		best_model = dbscan
		best_labels = dbscan_labels

	cluster_definitions: Dict[str, str] = {}
	if best_labels is not None:
		cluster_definitions = _summarize_clusters(X_df, best_labels)

	best_metrics = metrics.get(best_name, {})
	return {
		"best_model_name": best_name,
		"best_model": best_model,
		"best_metrics": best_metrics,
		"metrics": metrics,
		"cluster_definitions": cluster_definitions,
	}
