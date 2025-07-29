from fastapi import APIRouter, Depends, status

from app.api.models import User
from app.api.schemas import (
    SettingResponseSchema,
    SettingCreateSchema,
    SettingUpdateSchema,
)
from app.api.utils.jwt_handler import get_current_user
from app.api.controllers import SettingController

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
    responses={404: {"description": "Not found"}},
)


@router.get("", status_code=status.HTTP_200_OK, response_model=SettingResponseSchema)
async def get(
    current_user: User = Depends(get_current_user),
    setting_controller: SettingController = Depends(),
) -> SettingResponseSchema:
    return await setting_controller.get(current_user.id)


#
# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=SettingResponseSchema)
# async def post(
#         payload: SettingCreateSchema,
#         current_user: User = Depends(get_current_user),
#         setting_controller: SettingController = Depends()
# ) -> SettingResponseSchema:
#     return await setting_controller.post(current_user.id, payload=payload)


@router.put("/", status_code=status.HTTP_200_OK, response_model=SettingResponseSchema)
async def put(
    payload: SettingUpdateSchema,
    current_user: User = Depends(get_current_user),
    setting_controller: SettingController = Depends(),
) -> SettingResponseSchema:
    return await setting_controller.put(current_user.id, payload=payload)
