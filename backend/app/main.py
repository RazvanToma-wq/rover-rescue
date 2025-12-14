from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.map import router as map_router
from app.api.mission import router as mission_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(map_router)
app.include_router(mission_router)
