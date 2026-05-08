from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.decomposition import PCA


def apply_pca_if_needed(
	X_df: pd.DataFrame, feature_threshold: int = 50, random_state: int = 42
) -> tuple[pd.DataFrame, bool, PCA | None]:
	"""If total columns > feature_threshold, apply PCA to numeric columns so total cols <= threshold.

	Returns (transformed_df, pca_applied_flag, pca_object_or_none).
	"""
	if X_df.empty:
		return X_df.copy(), False, None

	total_cols = X_df.shape[1]
	if total_cols <= feature_threshold:
		return X_df.copy(), False, None

	numeric_cols = X_df.select_dtypes(include=["number"]).columns.tolist()
	non_numeric_count = total_cols - len(numeric_cols)
	if len(numeric_cols) == 0:
		return X_df.copy(), False, None

	max_pca_components = max(1, feature_threshold - non_numeric_count)
	n_components = min(len(numeric_cols), max_pca_components)

	# scale numeric cols before PCA
	scaler = StandardScaler()
	numeric_scaled = scaler.fit_transform(X_df[numeric_cols])

	pca = PCA(n_components=n_components, random_state=random_state)
	pca_arr = pca.fit_transform(numeric_scaled)
	pca_cols = [f"pca_{i+1}" for i in range(n_components)]
	pca_df = pd.DataFrame(pca_arr, columns=pca_cols, index=X_df.index)

	# preserve non-numeric columns
	non_numeric_df = X_df.drop(columns=numeric_cols)
	result = pd.concat([non_numeric_df, pca_df], axis=1)
	return result, True, pca


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
		# Drop obvious date/time-related columns and components (year/month/day)
		if (
			"date" in lower
			or "datetime" in lower
			or "timestamp" in lower
			or "year" in lower
			or "month" in lower
			or "day" in lower
		):
			cols_to_drop.append(col)
			continue

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


def remove_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
	"""Remove fully duplicated rows while preserving original index order."""
	if df.empty:
		return df

	return df.drop_duplicates(keep="first")


def one_hot_encode_categorical(
	df: pd.DataFrame,
	max_categories_per_column: int = 25,
	drop_high_unique_ratio: float | None = None,
) -> pd.DataFrame:
	"""One-hot encode categorical columns with safeguards for high cardinality.

	- Columns with too many categories are grouped into top-(k-1) + "__OTHER__".
	- Optional: near-unique high-cardinality columns (e.g., address-like IDs) can be dropped.
	"""
	if df.empty:
		return df

	categorical_cols = df.select_dtypes(include=["object", "category", "bool"]).columns
	if not len(categorical_cols):
		return df.copy()

	n_rows = max(len(df), 1)
	prepared_categorical: dict[str, pd.Series] = {}

	for col in categorical_cols:
		series = df[col].astype(str)
		unique_count = int(series.nunique(dropna=False))
		unique_ratio = unique_count / n_rows

		# Constant categorical columns carry no predictive information.
		if unique_count <= 1:
			continue

		# Optional identifier-like drop to avoid sparse, low-signal explosion.
		if (
			drop_high_unique_ratio is not None
			and unique_count > max_categories_per_column
			and unique_ratio >= drop_high_unique_ratio
		):
			continue

		if unique_count > max_categories_per_column:
			top_values = series.value_counts(dropna=False).head(max_categories_per_column - 1).index
			series = series.where(series.isin(top_values), "__OTHER__")

		prepared_categorical[col] = series

	numeric_df = df.drop(columns=list(categorical_cols))
	if not prepared_categorical:
		return numeric_df

	prepared_df = pd.DataFrame(prepared_categorical, index=df.index)
	encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
	encoded_array = encoder.fit_transform(prepared_df)
	encoded_cols = encoder.get_feature_names_out(prepared_df.columns)
	encoded_df = pd.DataFrame(encoded_array, columns=encoded_cols, index=df.index)

	return pd.concat([numeric_df, encoded_df], axis=1)


def get_high_cardinality_categorical_columns(
	df: pd.DataFrame,
	max_categories_per_column: int = 25,
) -> list[str]:
	"""Return categorical columns whose distinct values exceed the configured cap."""
	if df.empty:
		return []

	categorical_cols = df.select_dtypes(include=["object", "category", "bool"]).columns
	high_cardinality_cols: list[str] = []

	for col in categorical_cols:
		unique_count = int(df[col].astype(str).nunique(dropna=False))
		if unique_count > max_categories_per_column:
			high_cardinality_cols.append(str(col))

	return high_cardinality_cols


def remove_outliers(df: pd.DataFrame, iqr_multiplier: float = 1.5) -> pd.DataFrame:
	"""Remove rows with outliers in numeric columns using IQR method."""
	if df.empty:
		return df

	result = df.copy()
	numeric_cols = result.select_dtypes(include=["number"]).columns.tolist()

	if not numeric_cols:
		return result

	# Identify rows to drop
	rows_to_drop = set()
	for col in numeric_cols:
		q1 = result[col].quantile(0.25)
		q3 = result[col].quantile(0.75)
		iqr = q3 - q1

		if iqr == 0:
			continue

		lower = q1 - iqr_multiplier * iqr
		upper = q3 + iqr_multiplier * iqr

		outlier_indices = result[(result[col] < lower) | (result[col] > upper)].index
		rows_to_drop.update(outlier_indices)

	if rows_to_drop:
		result = result.drop(index=list(rows_to_drop))

	return result

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


def remove_correlated_features(df: pd.DataFrame, correlation_threshold: float = 0.85) -> pd.DataFrame:
	if df.empty:
		return df

	result = df.copy()
	numeric_cols = result.select_dtypes(include=["number"]).columns.tolist()

	if len(numeric_cols) < 2:
		return result

	corr_matrix = result[numeric_cols].corr().abs()

	cols_to_drop = set()
	for i in range(len(corr_matrix.columns)):
		for j in range(i + 1, len(corr_matrix.columns)):
			if corr_matrix.iloc[i, j] >= correlation_threshold:
				col_to_drop = corr_matrix.columns[j]
				cols_to_drop.add(col_to_drop)

	if cols_to_drop:
		result = result.drop(columns=list(cols_to_drop))

	return result


def _is_categorical_target(y) -> bool:
	series = y if isinstance(y, pd.Series) else pd.Series(y)
	return not pd.api.types.is_numeric_dtype(series)


def encode_target_labels(y: pd.Series):
	series = y if isinstance(y, pd.Series) else pd.Series(y)
	if pd.api.types.is_numeric_dtype(series):
		return series, None

	encoder = LabelEncoder()
	encoded = encoder.fit_transform(series.astype(str))
	return pd.Series(encoded, index=series.index), encoder


def is_target_imbalanced(
	y,
	minority_majority_ratio_threshold: float = 0.67,
	assume_classification: bool = False,
) -> bool:
	if not assume_classification and not _is_categorical_target(y):
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


def random_oversample(
	X,
	y,
	random_state: int = 42,
	assume_classification: bool = False,
):
	if not assume_classification and not _is_categorical_target(y):
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


def drop_rows_with_missing_target(X_df: pd.DataFrame, y) -> tuple[pd.DataFrame, pd.Series]:
	if X_df is None or X_df.empty:
		series_y = pd.Series(y) if not isinstance(y, pd.Series) else y.copy()
		return X_df.copy() if X_df is not None else pd.DataFrame(), series_y

	if isinstance(y, pd.Series):
		series_y = y.copy()
		if not series_y.index.equals(X_df.index) and len(series_y) == len(X_df):
			series_y.index = X_df.index
	else:
		try:
			series_y = pd.Series(y, index=X_df.index)
		except Exception:
			series_y = pd.Series(y)

	mask = ~series_y.isna()
	if mask.sum() == 0:
		raise ValueError("All target values are missing after preprocessing; cannot train.")

	X_clean = X_df.loc[mask]
	y_clean = series_y.loc[mask]

	return X_clean, y_clean
