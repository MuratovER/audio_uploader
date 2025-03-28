from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")


api_router = APIRouter(prefix="/api")
api_router.include_router(v1_router)
