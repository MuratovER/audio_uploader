from fastapi import APIRouter

from api.v1.uploader import router as audio_file_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(audio_file_router)

api_router = APIRouter(prefix="/api")
api_router.include_router(v1_router)
