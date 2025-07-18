from aiogram import Router

main_router = Router()

from .hello import router as hello_router

main_router.include_routers(hello_router)

__all__ = ("main_router",)
