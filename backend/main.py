from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import data, train, download

app = FastAPI()

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (configure more restrictively in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(data.data_router)
app.include_router(train.train_router)
app.include_router(download.download_router)
