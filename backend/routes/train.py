from __future__ import annotations

import sys
from pathlib import Path

from fastapi import APIRouter, Form, status
from fastapi.responses import JSONResponse

from controllers import TrainController
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

	return JSONResponse(
		content={
			"model_name": result.get("model_name"),
			"metrics": result.get("metrics"),
			"all_metrics": result.get("all_metrics"),
		},
	)