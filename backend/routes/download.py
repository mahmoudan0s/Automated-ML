from __future__ import annotations

from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import os

from controllers import ModelStorageController


download_router = APIRouter(
    prefix="/api/v1/download",
    tags=["api_v1", "download"],
)


@download_router.get("/model/{model_id}")
async def download_model(
    model_id: str,
    file_type: str = Query("joblib", enum=["joblib", "pkl"]),
):
    """
    Download a trained model with its preprocessing pipeline.

    Args:
        model_id: Unique identifier of the model
        file_type: File format - 'joblib' or 'pkl' (internally both use joblib)

    Returns:
        Downloadable model file
    """
    try:
        storage_controller = ModelStorageController()
        model_data = storage_controller.load_model(model_id)

        # The file path to return
        model_path = Path(model_data["model_path"])

        if not model_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Model file for ID '{model_id}' not found",
            )

        # Generate filename with extension
        filename = f"{model_id}.joblib"

        return FileResponse(
            path=model_path,
            filename=filename,
            media_type="application/octet-stream",
        )

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error downloading model: {str(e)}",
        )


@download_router.get("/preprocessor/{model_id}")
async def download_preprocessor(model_id: str):
    """
    Download the preprocessing pipeline for a model.

    Args:
        model_id: Unique identifier of the model

    Returns:
        Downloadable preprocessor file
    """
    try:
        storage_controller = ModelStorageController()
        model_data = storage_controller.load_model(model_id)

        preprocessor_path = Path(model_data["preprocessor_path"])

        if not preprocessor_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Preprocessor file for ID '{model_id}' not found",
            )

        filename = f"{model_id}_preprocessor.joblib"

        return FileResponse(
            path=preprocessor_path,
            filename=filename,
            media_type="application/octet-stream",
        )

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error downloading preprocessor: {str(e)}",
        )


@download_router.get("/model-package/{model_id}")
async def download_model_package(model_id: str):
    """
    Download a complete model package (model + preprocessor + metadata in a zip file).

    Args:
        model_id: Unique identifier of the model

    Returns:
        Downloadable zip file containing the complete model package
    """
    import zipfile
    import tempfile

    try:
        storage_controller = ModelStorageController()
        model_data = storage_controller.load_model(model_id)

        model_dir = Path(model_data["model_path"]).parent
        metadata = model_data["metadata"]

        # Create a temporary zip file
        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_zip:
            tmp_zip_path = tmp_zip.name

        try:
            with zipfile.ZipFile(tmp_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                # Add model
                zf.write(
                    Path(model_data["model_path"]),
                    arcname="model.joblib",
                )

                # Add preprocessor
                zf.write(
                    Path(model_data["preprocessor_path"]),
                    arcname="preprocessor.joblib",
                )

                # Add metadata
                import json

                metadata_json = json.dumps(metadata, indent=2)
                zf.writestr("metadata.json", metadata_json)

            return FileResponse(
                path=tmp_zip_path,
                filename=f"{model_id}_package.zip",
                media_type="application/zip",
            )

        except Exception as e:
            if os.path.exists(tmp_zip_path):
                os.remove(tmp_zip_path)
            raise e

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating model package: {str(e)}",
        )


@download_router.get("/models")
async def list_models():
    """
    List all available trained models.

    Returns:
        JSON with list of available models and their metadata
    """
    try:
        storage_controller = ModelStorageController()
        models = storage_controller.list_models()

        return JSONResponse(
            content={
                "count": len(models),
                "models": models,
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing models: {str(e)}",
        )


@download_router.delete("/model/{model_id}")
async def delete_model(model_id: str):
    """
    Delete a trained model and its preprocessor.

    Args:
        model_id: Unique identifier of the model

    Returns:
        JSON confirmation of deletion
    """
    try:
        storage_controller = ModelStorageController()
        storage_controller.delete_model(model_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "signal": f"Model '{model_id}' deleted successfully",
                "model_id": model_id,
            },
        )

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting model: {str(e)}",
        )
