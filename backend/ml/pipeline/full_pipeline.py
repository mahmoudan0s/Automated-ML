from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

import pandas as pd
from sklearn.pipeline import Pipeline

from ..preprocessing import build_preprocessor, split_features_target
from ..preprocessing.resampling import choose_sampler, is_target_imbalanced


@dataclass
class ModelPipelineArtifacts:
	pipeline: Pipeline
	numerical_features: List[str]
	ordered_categorical_features: List[str]
	unordered_categorical_features: List[str]
	imputation_strategy: str
	scaler_used: str
	sampler_used: Optional[str]


def build_pipeline_with_estimator(
	df: pd.DataFrame,
	target_column: str,
	model_name: str,
	estimator,
	ordered_categorical_features: Optional[Iterable[str]] = None,
	category_orders: Optional[Dict[str, List[Any]]] = None,
	correlation_threshold: float = 0.6,
) -> ModelPipelineArtifacts:
	preproc_artifacts = build_preprocessor(
		df=df,
		target_column=target_column,
		model_name=model_name,
		ordered_categorical_features=ordered_categorical_features,
		category_orders=category_orders,
		correlation_threshold=correlation_threshold,
	)
	pipeline = Pipeline(
		steps=[
			("preprocessor", preproc_artifacts.preprocessor),
			("model", estimator),
		]
	)
	return ModelPipelineArtifacts(
		pipeline=pipeline,
		numerical_features=preproc_artifacts.numerical_features,
		ordered_categorical_features=preproc_artifacts.ordered_categorical_features,
		unordered_categorical_features=preproc_artifacts.unordered_categorical_features,
		imputation_strategy=preproc_artifacts.imputation_strategy,
		scaler_used=preproc_artifacts.scaler_used,
		sampler_used=None,
	)


def fit_pipeline_with_estimator(
	df: pd.DataFrame,
	target_column: str,
	model_name: str,
	estimator,
	ordered_categorical_features: Optional[Iterable[str]] = None,
	category_orders: Optional[Dict[str, List[Any]]] = None,
	enable_resampling: bool = True,
	resampling_method: str = "random",
	imbalance_ratio_threshold: float = 0.67,
	correlation_threshold: float = 0.6,
	random_state: int = 42,
) -> ModelPipelineArtifacts:
	artifacts = build_pipeline_with_estimator(
		df=df,
		target_column=target_column,
		model_name=model_name,
		estimator=estimator,
		ordered_categorical_features=ordered_categorical_features,
		category_orders=category_orders,
		correlation_threshold=correlation_threshold,
	)

	X, y = split_features_target(df, target_column)

	if enable_resampling and is_target_imbalanced(y, minority_majority_ratio_threshold=imbalance_ratio_threshold):
		sampler, sampler_name = choose_sampler(preferred=resampling_method, random_state=random_state)
		if sampler is not None:
			preprocessor = artifacts.pipeline.named_steps["preprocessor"]
			model = artifacts.pipeline.named_steps["model"]

			X_processed = preprocessor.fit_transform(X, y)
			X_balanced, y_balanced = sampler.fit_resample(X_processed, y)
			model.fit(X_balanced, y_balanced)
			artifacts.sampler_used = sampler_name
			return artifacts

	artifacts.pipeline.fit(X, y)
	return artifacts


__all__ = [
	"ModelPipelineArtifacts",
	"build_pipeline_with_estimator",
	"fit_pipeline_with_estimator",
]
