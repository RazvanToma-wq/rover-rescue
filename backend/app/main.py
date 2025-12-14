from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.map import router as map_router
from app.api.mission import router as mission_router

app = FastAPI()

# ✅ FINAL CORS CONFIG (works on Vercel + browsers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allow all origins
    allow_credentials=False,      # MUST be False for browser compatibility
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(map_router)
app.include_router(mission_router)
