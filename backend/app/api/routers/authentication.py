from fastapi import APIRouter, Depends, status

from app.api.controllers.authentication_controller import AuthenticationController
from app.api.schemas.authentication_schema import (
    RefreshTokenSchema,
    TokenResponseSchema,
)
from app.api.schemas.user_schema import UserBase

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login/", status_code=status.HTTP_201_CREATED, response_model=TokenResponseSchema
)
async def login(
    payload: UserBase,
    controller: AuthenticationController = Depends(),
):
    return await controller.login(payload=payload)


@router.post(
    "/refresh/",
    response_model=TokenResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def refresh(
    payload: RefreshTokenSchema,
    controller: AuthenticationController = Depends(),
):
    return await controller.refresh(payload=payload)
