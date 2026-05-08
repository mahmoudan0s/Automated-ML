from .BaseController import BaseController
from .DataController import DataController


class TrainController(BaseController):
    def __init__(self):
        super().__init__()

    def load_training_dataframe(self, file_path: str):
        return DataController().load_dataframe(file_path)
