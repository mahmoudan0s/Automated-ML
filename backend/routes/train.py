from __future__ import annotations

import sys
from pathlib import Path

from fastapi import APIRouter, Form, status
from fastapi.responses import JSONResponse

from controllers import TrainController, ModelStorageController
from models import ProblemType, SUPERVISED_PROBLEMS

ML_SERVICES_DIR = Path(__file__).resolve().parents[1] / "ml-services"
if str(ML_SERVICES_DIR) not in sys.path:
	# Prepend to avoid clashing with backend.models
	sys.path.insert(0, str(ML_SERVICES_DIR))

# Clear conflicting modules so ml-services packages resolve correctly.
for module_name in ["models", "preprocessing"]:
	if module_name in sys.modules:
		del sys.modules[module_name]

from orchestrator import run_pipeline


def _humanize_model_name(model_name: str | None, problem_type: str | None = None) -> str:
	if not model_name:
		return ""

	if problem_type == "regression" and model_name == "linear":
		return "Linear Regression"
	if problem_type == "classification" and model_name == "logistic_regression":
		return "Logistic Regression"

	label = model_name.replace("_", " ")
	label = label.replace("svm ", "SVM ")
	label = label.replace("r2", "R²")

	parts = label.split()
	formatted_parts = []
	for part in parts:
		if part.lower() == "svm":
			formatted_parts.append("SVM")
		elif part.lower() == "linear":
			formatted_parts.append("Linear")
		elif part.lower() == "random":
			formatted_parts.append("Random")
		elif part.lower() == "forest":
			formatted_parts.append("Forest")
		elif part.lower() == "logistic":
			formatted_parts.append("Logistic")
		elif part.lower() == "regression":
			formatted_parts.append("Regression")
		elif part.lower() == "classification":
			formatted_parts.append("Classification")
		elif part.lower() == "rbf":
			formatted_parts.append("RBF")
		elif part.lower() == "poly":
			formatted_parts.append("Poly")
		elif part.lower() == "alpha":
			formatted_parts.append("alpha")
		else:
			formatted_parts.append(part[:1].upper() + part[1:])

	return " ".join(formatted_parts)


def _build_model_display_names(all_models: list[str] | None, problem_type: str | None = None) -> dict[str, str]:
	if not all_models:
		return {}

	return {model_name: _humanize_model_name(model_name, problem_type) for model_name in all_models}


train_router = APIRouter(
	prefix="/api/v1/train",
	tags=["api_v1", "train"],
)


@train_router.post("/run")
async def train_model(
	file_path: str = Form(...),
	problem_type: ProblemType = Form(...),
	target_column: str | None = Form(None),
):
	if problem_type in SUPERVISED_PROBLEMS and not target_column:
		return JSONResponse(
			status_code=status.HTTP_400_BAD_REQUEST,
			content={"signal": "target_column is required for supervised tasks"},
		)

	df = TrainController().load_training_dataframe(file_path)
	result = run_pipeline(df, task=problem_type.value, target=target_column)

	# Format metrics for consistent frontend display
	def _format_value(key: str, val):
		percent_keys = {"accuracy", "precision", "recall", "f1_score", "f1", "auc"}
		# Keep non-numeric types as-is (lists, dicts)
		if isinstance(val, (list, dict)):
			return val
		try:
			if isinstance(val, (int, float)) and not isinstance(val, bool):
				if key.lower() in percent_keys:
					# assume value in [0,1], convert to percent
					return f"{(val * 100):.1f}%"
				# not a percentage
				return f"{val:.3f}"
			# strings that may end with % or be numeric
			if isinstance(val, str):
				trim = val.strip()
				if trim.endswith("%"):
					try:
						n = float(trim[:-1])
						return f"{n:.1f}%"
					except Exception:
						return val
				# numeric string
				try:
					n = float(trim)
					if key.lower() in percent_keys:
						return f"{(n * 100):.1f}%"
					return f"{n:.3f}"
				except Exception:
					return val
		except Exception:
			return val

	def _format_metrics(metrics_obj):
		if metrics_obj is None:
			return None
		# metrics_obj expected to be a dict mapping model_name -> {metric_key: value}
		formatted = {}
		for model_name, metrics in metrics_obj.items():
			if isinstance(metrics, dict):
				formatted_metrics = {}
				for k, v in metrics.items():
					formatted_metrics[k] = _format_value(k, v)
				formatted[model_name] = formatted_metrics
			else:
				formatted[model_name] = metrics
		return formatted

	formatted_metrics = _format_metrics(result.get("metrics"))
	formatted_all_metrics = _format_metrics(result.get("all_metrics"))
	formatted_best_metrics = None
	if isinstance(result.get("best_metrics"), dict):
		formatted_best_metrics = {k: _format_value(k, v) for k, v in result.get("best_metrics").items()}

	model_display_names = _build_model_display_names(result.get("all_models"), problem_type.value)

	# Save model and preprocessor with formatted metrics in metadata
	storage_controller = ModelStorageController()
	model_id = storage_controller.save_model(
		model=result.get("model"),
		preprocessor=result.get("preprocessor"),
		model_name=result.get("model_name"),
		problem_type=problem_type.value,
		metadata={
			"metrics": formatted_best_metrics,
			"model_display_name": model_display_names.get(result.get("model_name"), result.get("model_name")),
		},
	)

	response_content = {
		"model_id": model_id,
		"model_name": result.get("model_name"),
		"model_display_name": model_display_names.get(result.get("model_name"), result.get("model_name")),
		"metrics": formatted_best_metrics,
		"all_metrics": formatted_all_metrics,
		"all_models": result.get("all_models"),
		"model_display_names": model_display_names,
		"feature_importance": result.get("feature_importance"),
	}

	cluster_definitions = result.get("cluster_definitions")
	if cluster_definitions is not None:
		response_content["cluster_definitions"] = cluster_definitions

	scatter_points = result.get("scatter_points")
	if scatter_points is not None:
		response_content["scatter_points"] = scatter_points

	roc_curve = result.get("roc_curve")
	if roc_curve is not None:
	    response_content["roc_curve"] = roc_curve

	return JSONResponse(content=response_content)