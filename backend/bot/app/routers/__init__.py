from aiogram import Router

from .start import start_router
from .demo import demo_router
from .channel import channel_router

main_router = Router()

main_router.include_router(channel_router)
main_router.include_router(start_router)
main_router.include_router(demo_router)

__all__ = ["main_router"]
