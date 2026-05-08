from __future__ import annotations

from typing import Any, Optional, Tuple

import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

from models.classification import train_classification
from models.clustering import train_clustering
from models.regression import train_regression
from preprocessing.preprocessing import (
	encode_target_labels,
	get_high_cardinality_categorical_columns,
	impute_missing_values,
	is_target_imbalanced,
	one_hot_encode_categorical,
	random_oversample,
	remove_correlated_features,
	remove_duplicate_rows,
	remove_outliers,
	scale_numeric_features,
    drop_rows_with_missing_target,
)


def _group_importance_by_original_columns(
	ranked_features: list[tuple[str, float]],
	original_feature_names: list[str],
	columns_to_group: Optional[set[str]] = None,
) -> list[dict[str, float | str]]:
	if not ranked_features:
		return []

	grouped: dict[str, float] = {}

	for encoded_name, score in ranked_features:
		group_name = encoded_name

		if encoded_name not in original_feature_names:
			matched = [
				col for col in original_feature_names if encoded_name.startswith(f"{col}_")
			]
			if matched:
				# Prefer the longest match to avoid prefix collisions.
				candidate = max(matched, key=len)
				if columns_to_group is None or candidate in columns_to_group:
					group_name = candidate

		grouped[group_name] = grouped.get(group_name, 0.0) + float(score)

	return [
		{"name": name, "importance": round(float(score), 4)}
		for name, score in sorted(grouped.items(), key=lambda item: item[1], reverse=True)
	]


def _extract_feature_importance(
	model: Any,
	X_eval,
	y_eval,
	feature_names: list[str],
	original_feature_names: Optional[list[str]] = None,
	high_cardinality_columns: Optional[list[str]] = None,
) -> list[dict[str, float | str]]:
	if not feature_names:
		return []

	if X_eval is None or y_eval is None:
		return []

	import numpy as np

	try:
		result = permutation_importance(
			model,
			X_eval,
			y_eval,
			n_repeats=5,
			random_state=42,
			scoring=None,
		)
	except Exception:
		return []

	values = np.asarray(result.importances_mean)
	if len(values) != len(feature_names):
		return []

	normalized = np.clip(values, 0, None)
	total = normalized.sum()
	normalized = normalized / total if total > 0 else normalized

	ranked = sorted(zip(feature_names, normalized), key=lambda item: item[1], reverse=True)

	if original_feature_names:
		return _group_importance_by_original_columns(
			ranked,
			original_feature_names,
			set(high_cardinality_columns) if high_cardinality_columns else None,
		)

	return [
		{"name": name, "importance": round(float(score), 4)}
		for name, score in ranked
	]


def preprocess(
	df: pd.DataFrame,
	target: Optional[str],
	task: str,
) -> Tuple[Any, Any, Pipeline, list[str], list[str], list[str]]:
	df = remove_duplicate_rows(df)

	supervised_tasks = {"classification", "regression"}
	if task in supervised_tasks:
		if not target or target not in df.columns:
			raise ValueError("target column is required and must exist in the dataset")
		y = df[target]
		X = df.drop(columns=[target])
	else:
		y = None
		X = df.copy()

	original_feature_names = list(X.columns.astype(str)) if hasattr(X, "columns") else []
	high_cardinality_columns = (
		get_high_cardinality_categorical_columns(X) if hasattr(X, "columns") else []
	)

	preprocessor = Pipeline(
		steps=[
			("impute", FunctionTransformer(impute_missing_values, validate=False)),
			("encode", FunctionTransformer(one_hot_encode_categorical, validate=False)),
			("scale", FunctionTransformer(scale_numeric_features, validate=False)),
			("remove_correlated", FunctionTransformer(remove_correlated_features, validate=False)),
		]
	)

	X = preprocessor.fit_transform(X)
	feature_names = (
		list(X.columns.astype(str))
		if hasattr(X, "columns")
		else [f"feature_{i}" for i in range(X.shape[1])]
	)
	if y is not None and hasattr(X, "index"):
		y = y.loc[X.index]

	if len(X) == 0:
		raise ValueError(
			"All rows were dropped during preprocessing. Adjust missing-value thresholds."
		)

	if task == "classification" and y is not None:
		y, _label_encoder = encode_target_labels(y)

	return X, y, preprocessor, feature_names, original_feature_names, high_cardinality_columns


def run_pipeline(df, task, target=None):
	X, y, preprocessor, feature_names, original_feature_names, high_cardinality_columns = preprocess(
		df, target, task
	)

	if task == "regression":
		X_reg = remove_outliers(X)
		if y is not None and hasattr(X_reg, "index") and hasattr(y, "loc"):
			y_reg = y.loc[X_reg.index]
		else:
			y_reg = y

		# drop rows with missing target values
		if y_reg is not None:
			X_reg, y_reg = drop_rows_with_missing_target(X_reg, y_reg)

		if len(X_reg) < 2:
			raise ValueError(
				"Outlier removal left fewer than 2 rows for regression training."
			)

		result = train_regression(X_reg, y_reg)
		return {
			"model": result["best_model"],
			"model_name": result["best_model_name"],
			"metrics": result["best_metrics"],
			"all_metrics": result["metrics"],
			"all_models": list(result["metrics"].keys()),
			"preprocessor": preprocessor,
			"feature_names": feature_names,
			"feature_importance": _extract_feature_importance(
				result["best_model"],
				X_reg,
				y_reg,
				feature_names,
				original_feature_names,
				high_cardinality_columns,
			),
		}

	if task == "classification":
		X_cls = remove_outliers(X)
		if y is not None and hasattr(X_cls, "index") and hasattr(y, "loc"):
			y_cls = y.loc[X_cls.index]
		else:
			y_cls = y

		# drop rows with missing target values
		if y_cls is not None:
			X_cls, y_cls = drop_rows_with_missing_target(X_cls, y_cls)

		if is_target_imbalanced(y_cls, assume_classification=True):
			X_array = X_cls.to_numpy() if hasattr(X_cls, "to_numpy") else X_cls
			X_resampled, y_resampled = random_oversample(
				X_array,
				y_cls,
				assume_classification=True,
			)
			X_cls = (
				pd.DataFrame(X_resampled, columns=list(X.columns), index=None)
				if hasattr(X, "columns")
				else X_resampled
			)
			y_cls = y_resampled

		result = train_classification(X_cls, y_cls)
		# Attempt to compute ROC curve & AUC for binary classification when possible
		roc_payload = None
		try:
			import numpy as _np

			y_true = y_cls
			best_model = result.get("best_model")
			scores = None

			if best_model is not None:
				if hasattr(best_model, "predict_proba"):
					probs = best_model.predict_proba(X_cls)
					# if multiclass, take class 1 column when applicable
					if probs.ndim == 2 and probs.shape[1] >= 2:
						scores = probs[:, 1]
					else:
						scores = probs.ravel()
				elif hasattr(best_model, "decision_function"):
					scores = best_model.decision_function(X_cls)

			# Only compute ROC for binary targets
			if scores is not None and _np.unique(y_true).size == 2:
				fpr_vals, tpr_vals, _ = roc_curve(y_true, scores)
				auc_val = float(roc_auc_score(y_true, scores))
				points = [
					{"fpr": round(float(f), 3), "tpr": round(float(t), 3)}
					for f, t in zip(fpr_vals, tpr_vals)
				]
				roc_payload = {"points": points, "auc": round(auc_val, 4)}
		except Exception:
			roc_payload = None

		return {
			"model": result["best_model"],
			"model_name": result["best_model_name"],
			"metrics": result["best_metrics"],
			"all_metrics": result["metrics"],
			"all_models": list(result["metrics"].keys()),
			"preprocessor": preprocessor,
			"feature_names": feature_names,
			"feature_importance": _extract_feature_importance(
				result["best_model"],
				X_cls,
				y_cls,
				feature_names,
				original_feature_names,
				high_cardinality_columns,
			),
			"roc_curve": roc_payload,
		}

	if task == "clustering":
		result = train_clustering(X)
		return {
			"model": result["best_model"],
			"model_name": result["best_model_name"],
			"metrics": result["best_metrics"],
			"all_metrics": result["metrics"],
			"all_models": list(result["metrics"].keys()),
			"cluster_definitions": result["cluster_definitions"],
			"scatter_points": result.get("scatter_points"),
			"preprocessor": preprocessor,
			"feature_names": feature_names,
		}

	raise ValueError("Invalid task type")
