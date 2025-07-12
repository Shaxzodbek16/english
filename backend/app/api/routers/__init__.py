from fastapi import APIRouter
from app.core.settings import get_settings, Settings
from .healthcheck import router as healthcheck_router
from .channel import router as channel_router
from .authentication import router as auth_router
from .user_router import router as user_router
from .admin_user_router import router as admin_user_router

settings: Settings = get_settings()

main_router = APIRouter(
    prefix=settings.API_V1_STR,
)

main_router.include_router(channel_router)
main_router.include_router(auth_router)
main_router.include_router(user_router)
main_router.include_router(admin_user_router)
main_router.include_router(healthcheck_router)

__all__ = ["main_router"]
