from fastapi import FastAPI
from routes import data, train

app = FastAPI()

app.include_router(data.data_router)
app.include_router(train.train_router)
