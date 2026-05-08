from __future__ import annotations

from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering, DBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler


def _choose_k_by_silhouette(
	X: np.ndarray,
	k_min: int = 2,
	k_max: int = 15,
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


def _build_scatter_points(X_df: pd.DataFrame, labels: np.ndarray) -> Dict[str, Any]:
	if X_df.empty:
		return {"x_axis": "x", "y_axis": "y", "clusters": []}

	feature_names = list(X_df.columns.astype(str))
	x_axis = feature_names[0]
	y_axis = feature_names[1] if len(feature_names) > 1 else feature_names[0]

	clusters: Dict[str, Dict[str, Any]] = {}
	for row_index, label in enumerate(labels):
		cluster_id = int(label)
		cluster_key = str(cluster_id)
		if cluster_key not in clusters:
			clusters[cluster_key] = {"id": cluster_id, "members": []}

		row = X_df.iloc[row_index]
		x_value = row.iloc[0]
		y_value = row.iloc[1] if len(row) > 1 else row.iloc[0]
		clusters[cluster_key]["members"].append(
			{
				x_axis: round(float(x_value), 2),
				y_axis: round(float(y_value), 2),
			}
		)

	return {
		"x_axis": x_axis,
		"y_axis": y_axis,
		"clusters": list(clusters.values()),
	}


def train_clustering(X: pd.DataFrame) -> Dict[str, Any]:
	X_df = X.copy()
	X_array = X_df.to_numpy()

	# scale features before clustering
	scaler = StandardScaler()
	X_scaled = scaler.fit_transform(X_array)

	# project the full feature space to 2D for visualization
	pca = PCA(n_components=2, random_state=42)
	X_pca = pca.fit_transform(X_scaled)
	pca_df = pd.DataFrame(X_pca, columns=["pca_1", "pca_2"], index=X_df.index)

	metrics: Dict[str, Dict[str, Any]] = {}
	best_name = None
	best_model = None
	best_score = float("-inf")
	best_labels: np.ndarray | None = None

	k_best, k_score = _choose_k_by_silhouette(X_scaled, k_min=2, k_max=15)
	if k_best is not None:
		kmeans = KMeans(n_clusters=k_best, random_state=42, n_init=10)
		labels = kmeans.fit_predict(X_scaled)
		score = silhouette_score(X_scaled, labels)
		dbi = davies_bouldin_score(X_scaled, labels)
		metrics["kmeans"] = {
			"silhouette": score,
			"n_clusters": k_best,
			"inertia": kmeans.inertia_,
			"davies_bouldin_index": dbi,
		}
		if score > best_score:
			best_score = score
			best_name = "kmeans"
			best_model = kmeans
			best_labels = labels

	if k_best is not None:
		agglom = AgglomerativeClustering(n_clusters=k_best)
		labels = agglom.fit_predict(X_scaled)
		if len(set(labels)) > 1:
			score = silhouette_score(X_scaled, labels)
			dbi = davies_bouldin_score(X_scaled, labels)
			metrics["agglomerative"] = {
				"silhouette": score,
				"n_clusters": k_best,
				"davies_bouldin_index": dbi,
			}
			if score > best_score:
				best_score = score
				best_name = "agglomerative"
				best_model = agglom
				best_labels = labels

	dbscan = DBSCAN(eps=0.5, min_samples=5)
	dbscan_labels = dbscan.fit_predict(X_scaled)
	unique_labels = set(dbscan_labels)
	n_clusters = len([lbl for lbl in unique_labels if lbl != -1])
	if n_clusters >= 2:
		score = silhouette_score(X_scaled, dbscan_labels)
		dbi = davies_bouldin_score(X_scaled, dbscan_labels)
	else:
		score = float("-inf")
		dbi = float("inf")

	metrics["dbscan"] = {
		"silhouette": score if score != float("-inf") else None,
		"n_clusters": n_clusters,
		"noise_points": int((dbscan_labels == -1).sum()),
		"davies_bouldin_index": dbi if dbi != float("inf") else None,
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
	scatter_points = _build_scatter_points(pca_df, best_labels) if best_labels is not None else None
	return {
		"best_model_name": best_name,
		"best_model": best_model,
		"best_metrics": best_metrics,
		"metrics": metrics,
		"cluster_definitions": cluster_definitions,
		"scatter_points": scatter_points,
	}
