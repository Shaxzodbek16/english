import os
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
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

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.errors(), "body": exc.body},
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
