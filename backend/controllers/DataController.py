import os
import re
from .BaseController import BaseController  
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import pandas as pd

class DataController(BaseController):

    def __init__(self):
        super().__init__()
        self.size_scale= 1024 * 1024  # Convert bytes to MB

    def validate_upladed_file(self,file: UploadFile):

        allowed_extensions = {".csv", ".xls", ".xlsx"}
        filename = (file.filename or "").lower()
        if not filename.endswith(tuple(allowed_extensions)):
            return False,ResponseSignal.FILE_TYPE_NOT_ALLOWED.value

        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:

            #raise ValueError(f"File type {file.content_type} is not allowed. Allowed types: {self.app_settings.FILE_ALLOWED_TYPES}")
            return False,ResponseSignal.FILE_TYPE_NOT_ALLOWED.value
        if file.size > self.app_settings.FILE_MAX_SIZE_MB * self.size_scale:

            #raise ValueError(f"File size exceeds the maximum allowed size of {self.app_settings.FILE_MAX_SIZE_MB} MB.")
            return False,ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True,ResponseSignal.FILE_VALIDATED_SUCCESS.value
    
    def generate_unique_filename(self, original_filename: str, project_id: str):
        project_path = ProjectController().get_project_path(project_id=project_id)

        cleaned_filename = self.get_clean_filename(original_filename=original_filename)
        name, ext = os.path.splitext(cleaned_filename)

        # Start with the original filename
        candidate = f"{name}{ext}"
        new_file_path = os.path.join(project_path, candidate)

        # If already exists, append a short 3-char alphanumeric id and retry
        while os.path.exists(new_file_path):
            short_id = self.generate_random_string(length=3)
            candidate = f"{name}_{short_id}{ext}"
            new_file_path = os.path.join(project_path, candidate)

        return new_file_path
    
    def get_clean_filename(self, original_filename: str):
        # Remove any characters that are not alphanumeric, underscores, or dots
        cleaned_filename = re.sub(r'[^a-zA-Z0-9_.]', '', original_filename.strip())
        cleaned_filename = cleaned_filename.replace(" ", "_")  # Replace spaces with underscores
        return cleaned_filename

    def load_dataframe(self, file_path: str) -> pd.DataFrame:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File does not exist: {file_path}")

        _, ext = os.path.splitext(file_path.lower())
        if ext == ".csv":
            return pd.read_csv(file_path)
        if ext in {".xls", ".xlsx"}:
            return pd.read_excel(file_path)

        raise ValueError("Unsupported file format. Use .csv, .xls, or .xlsx")