from fastapi import Depends, status, HTTPException

from app.api.schemas import (
    SettingResponseSchema,
    SettingCreateSchema,
    SettingUpdateSchema,
)
from app.api.repositories import SettingRepository


class SettingController:
    def __init__(self, setting_repository: SettingRepository = Depends()):
        self.setting_repository = setting_repository

    async def get(self, user_id: int) -> SettingResponseSchema:
        setting = await self.setting_repository.get(user_id)
        if not setting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Settings not found for the user.",
            )
        return SettingResponseSchema.model_validate(setting)

    async def post(
        self, user_id: int, payload: SettingCreateSchema
    ) -> SettingResponseSchema:
        setting = await self.setting_repository.post(payload, user_id)
        return SettingResponseSchema.model_validate(setting)

    async def put(
        self, user_id: int, payload: SettingUpdateSchema
    ) -> SettingResponseSchema:
        setting = await self.setting_repository.put(payload, user_id)
        return SettingResponseSchema.model_validate(setting)
