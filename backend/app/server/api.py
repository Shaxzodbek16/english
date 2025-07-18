import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routers import main_router


def get_ready() -> None:
    os.makedirs("media/", exist_ok=True)
    os.makedirs("static/", exist_ok=True)


def get_app() -> FastAPI:
    get_ready()
    app = FastAPI(
        title="EnglishAI",
        description="An AI-powered English learning platform",
        version="1.0.0",
    )
    app.include_router(main_router)
    return app


def create_app() -> CORSMiddleware:
    app = get_app()
    return CORSMiddleware(
        app,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
