from fastapi import APIRouter, status, Depends, HTTPException

from app.api.controllers import UserController
from app.api.models import User
from app.api.schemas import (
    UserResponseSchema,
    UserListResponseSchema,
    QueryParamsSchema,
    UserUpdateSchema,
)
from app.api.utils.admin_filter import check_admin
from app.api.utils.jwt_handler import get_current_user
from app.core.settings import Settings, get_settings

settings: Settings = get_settings()

router = APIRouter(
    prefix="/admin-user", tags=["Admin User"], dependencies=[Depends(check_admin)]
)


@router.get("", status_code=status.HTTP_200_OK, response_model=UserListResponseSchema)
async def list_users(
    params: QueryParamsSchema = Depends(),
    user_controller: UserController = Depends(),
):
    return await user_controller.list(params=params)


@router.put(
    "/{phone_number}/",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseSchema,
)
async def update(
    phone_number: int,
    payload: UserUpdateSchema,
    current_user: User = Depends(get_current_user),
    user_controller: UserController = Depends(),
):
    if payload.is_admin:
        if current_user.telegram_id not in settings.ADMINS_TG_IDS:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action. Tell Shaxzodbek or Jasurbek to update the user.",
            )
    return await user_controller.update(phone_number=phone_number, payload=payload)
