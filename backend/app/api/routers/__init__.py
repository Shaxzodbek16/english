from fastapi import APIRouter
from app.core.settings import get_settings, Settings
from .healthcheck import router as healthcheck_router
from .channel import router as channel_router

settings: Settings = get_settings()

main_router = APIRouter(
    prefix=settings.API_V1_STR,
)

main_router.include_router(healthcheck_router)
main_router.include_router(channel_router)

__all__ = ["main_router"]
