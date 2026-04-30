from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder, OneHotEncoder


def impute_missing_values(
	df: pd.DataFrame,
	row_drop_threshold: float = 0.05,
	col_drop_threshold: float = 0.60,
) -> pd.DataFrame:
	"""Drop columns/rows by missing rate; otherwise impute."""
	if df.empty:
		return df

	result = df.copy()
	column_names = result.columns.astype(str)
	cols_to_drop = []
	for col in column_names:
		lower = col.lower()
		if lower == "id" or lower.endswith("_id") or "id" in col:
			cols_to_drop.append(col)
			continue
		if "date" in lower or "datetime" in lower or "timestamp" in lower:
			cols_to_drop.append(col)

	if cols_to_drop:
		result = result.drop(columns=list(set(cols_to_drop)))
	col_missing_rate = result.isna().mean()
	cols_to_drop = col_missing_rate[col_missing_rate > col_drop_threshold].index
	if len(cols_to_drop):
		result = result.drop(columns=list(cols_to_drop))

	row_missing_rate = result.isna().mean(axis=1)
	rows_to_drop = row_missing_rate[(row_missing_rate > 0) & (row_missing_rate <= row_drop_threshold)].index
	if len(rows_to_drop):
		result = result.drop(index=rows_to_drop)

	numeric_cols = result.select_dtypes(include=["number"]).columns
	categorical_cols = result.select_dtypes(include=["object", "category", "bool"]).columns

	for col in numeric_cols:
		mean_value = result[col].mean()
		result[col] = result[col].fillna(mean_value)

	for col in categorical_cols:
		mode_series = result[col].mode(dropna=True)
		if not mode_series.empty:
			result[col] = result[col].fillna(mode_series.iloc[0])

	return result


def one_hot_encode_categorical(df: pd.DataFrame) -> pd.DataFrame:
	"""One-hot encode categorical columns only."""
	if df.empty:
		return df

	categorical_cols = df.select_dtypes(include=["object", "category", "bool"]).columns
	if not len(categorical_cols):
		return df.copy()

	encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
	encoded_array = encoder.fit_transform(df[categorical_cols])
	encoded_cols = encoder.get_feature_names_out(categorical_cols)
	encoded_df = pd.DataFrame(encoded_array, columns=encoded_cols, index=df.index)

	numeric_df = df.drop(columns=list(categorical_cols))
	return pd.concat([numeric_df, encoded_df], axis=1)


def scale_numeric_features(df: pd.DataFrame) -> pd.DataFrame:
	"""Scale numeric features: robust scaler if outliers exist, else min-max."""
	if df.empty:
		return df

	result = df.copy()
	numeric_cols = result.select_dtypes(include=["number"]).columns
	if not len(numeric_cols):
		return result

	# Detect outliers using IQR per column.
	has_outliers = False
	for col in numeric_cols:
		q1 = result[col].quantile(0.25)
		q3 = result[col].quantile(0.75)
		iqr = q3 - q1
		if iqr == 0:
			continue
		lower = q1 - 1.5 * iqr
		upper = q3 + 1.5 * iqr
		if ((result[col] < lower) | (result[col] > upper)).any():
			has_outliers = True
			break

	if has_outliers:
		for col in numeric_cols:
			median = result[col].median()
			q1 = result[col].quantile(0.25)
			q3 = result[col].quantile(0.75)
			iqr = q3 - q1
			if iqr == 0:
				result[col] = result[col] - median
			else:
				result[col] = (result[col] - median) / iqr
		return result

	for col in numeric_cols:
		col_min = result[col].min()
		col_max = result[col].max()
		if col_max == col_min:
			result[col] = 0.0
		else:
			result[col] = (result[col] - col_min) / (col_max - col_min)

	return result


def _is_categorical_target(y) -> bool:
	series = y if isinstance(y, pd.Series) else pd.Series(y)
	return not pd.api.types.is_numeric_dtype(series)


def encode_target_labels(y: pd.Series):
	"""Encode categorical target labels."""
	series = y if isinstance(y, pd.Series) else pd.Series(y)
	if pd.api.types.is_numeric_dtype(series):
		return series, None

	encoder = LabelEncoder()
	encoded = encoder.fit_transform(series.astype(str))
	return pd.Series(encoded, index=series.index), encoder


def is_target_imbalanced(y, minority_majority_ratio_threshold: float = 0.67) -> bool:
	if not _is_categorical_target(y):
		return False

	y_array = np.asarray(y)
	unique, counts = np.unique(y_array, return_counts=True)
	if len(unique) < 2:
		return False

	min_count = counts.min()
	max_count = counts.max()
	if max_count == 0 or max_count == min_count:
		return False

	ratio = min_count / max_count
	return ratio < minority_majority_ratio_threshold


def random_oversample(X, y, random_state: int = 42):
	if not _is_categorical_target(y):
		return X, np.asarray(y)

	rng = np.random.RandomState(random_state)
	y_array = np.asarray(y)

	unique, counts = np.unique(y_array, return_counts=True)
	if len(unique) < 2:
		return X, y_array

	max_count = counts.max()
	indices = np.arange(len(y_array))
	resampled_indices = []

	for cls, count in zip(unique, counts):
		cls_indices = indices[y_array == cls]
		if count < max_count:
			extra = rng.choice(cls_indices, size=max_count - count, replace=True)
			cls_indices = np.concatenate([cls_indices, extra])
		resampled_indices.append(cls_indices)

	final_indices = np.concatenate(resampled_indices)
	rng.shuffle(final_indices)

	X_resampled = X[final_indices]
	y_resampled = y_array[final_indices]
	return X_resampled, y_resampled


def choose_sampler(random_state: int = 42):
	return "random", random_state
