from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException, status

from app.api.models import Setting
from app.api.schemas import SettingCreateSchema, SettingUpdateSchema
from app.core.databases.postgres import get_general_session


class SettingRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.__session = session

    async def get(self, user_id: int) -> Setting | None:
        setting = await self.__session.execute(select(Setting).where(Setting.user_id == user_id))
        return setting.scalar_one_or_none()

    async def post(self, setting: SettingCreateSchema, user_id) -> Setting:
        setting = Setting(
            user_id=user_id,
            settings=setting.settings if setting.settings else {}
        )
        self.__session.add(setting)

        try:
            await self.__session.commit()
            await self.__session.refresh(setting)
        except Exception as e:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saving setting: {str(e)}"
            )
        return setting

    async def put(self, setting: SettingUpdateSchema, user_id: int) -> Setting:
        existing_setting = await self.get(user_id)
        if not existing_setting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Setting not found."
            )

        existing_setting.update(setting.settings)

        try:
            await self.__session.commit()
            await self.__session.refresh(existing_setting)
        except Exception as e:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating setting: {str(e)}"
            )

        return existing_setting