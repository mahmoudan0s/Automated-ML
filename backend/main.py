from fastapi import FastAPI
from routes import data

app = FastAPI()

app.include_router(data.data_router)