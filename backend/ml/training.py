from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

import pandas as pd

from .models import ModelPipelineArtifacts, fit_model_pipeline


def train_with_full_pipeline(
	df: pd.DataFrame,
	target_column: str,
	model_name: str,
	ordered_categorical_features: Optional[Iterable[str]] = None,
	category_orders: Optional[Dict[str, List[Any]]] = None,
	enable_resampling: bool = True,
	resampling_method: str = "random",
	random_state: int = 42,
) -> ModelPipelineArtifacts:
	"""
	Create and fit an end-to-end ML pipeline that can be reused from any module.
	"""
	return fit_model_pipeline(
		df=df,
		target_column=target_column,
		model_name=model_name,
		ordered_categorical_features=ordered_categorical_features,
		category_orders=category_orders,
		enable_resampling=enable_resampling,
		resampling_method=resampling_method,
		random_state=random_state,
	)
