from fastapi import APIRouter, status, Depends

from app.api.controllers import UserController
from app.api.models import User
from app.api.schemas import (
    UserResponseSchema,
    UserListResponseSchema,
    QueryParamsSchema,
)
from app.api.utils.jwt_handler import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.get("/me", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
async def me(
    current_user: User = Depends(get_current_user),
    user_controller: UserController = Depends(),
):
    return await user_controller.get(current_user.phone_number)


@router.get(
    "/phone/{phone_number}",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_user(phone_number: int, user_controller: UserController = Depends()):
    return await user_controller.get(phone_number=phone_number)


@router.get(
    "/tg_id/{telegram_id}",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user)],
)
async def get_user_by_telegram_id(
    telegram_id: int, user_controller: UserController = Depends()
):
    return await user_controller.get_by_telegram_id(telegram_id=telegram_id)
