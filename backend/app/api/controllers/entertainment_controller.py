import os

from fastapi import Depends, HTTPException, status
from aiogram.types import FSInputFile, Message

from app.api.bot.main import get_bot
from app.api.repositories import EntertainmentRepository, EntertainmentTypeRepository

from app.core.settings import get_settings, Settings
from app.api.schemas import (
    EntertainmentQuerySchema,
    EntertainmentListResponseSchema,
    EntertainmentResponseSchema,
    EntertainmentCreateSchema,
    EntertainmentUpdate,
)


class EntertainmentController:
    def __init__(
            self,
            entertainment_repo: EntertainmentRepository = Depends(),
            entertainment_type_repo: EntertainmentTypeRepository = Depends(),
    ):
        self.__entertainment_repo = entertainment_repo
        self.__entertainment_type_repo = entertainment_type_repo
        self.__settings: Settings = get_settings()

    async def list_(
            self, query: EntertainmentQuerySchema
    ) -> EntertainmentListResponseSchema:
        entertainments = await self.__entertainment_repo.list_(query)
        if not entertainments:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="Not entertainments yet",
            )
        return EntertainmentListResponseSchema(
            page=query.page,
            size=query.size,
            search=query.search,
            filter=query.filter,
            sort=query.sort,
            total=len(entertainments),
            items=[
                EntertainmentResponseSchema.model_validate(entertainment)
                for entertainment in entertainments
            ],
        )

    async def get(self, entertainment_id: int) -> EntertainmentResponseSchema:
        entertainment = await self.__entertainment_repo.get(entertainment_id)
        if not entertainment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entertainment not found",
            )
        return EntertainmentResponseSchema.model_validate(entertainment)

    @staticmethod
    def _clear_file(file_path: str) -> None:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to delete file: {str(e)}",
                )

    async def _validate_entertainment_type(self, type_id: int | None) -> None:
        if type_id is not None:
            entertainment_type = await self.__entertainment_type_repo.get(type_id)
            if not entertainment_type:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Entertainment type not found",
                )

    async def _upload_to_telegram(
            self, /, *, media_path: str, media_type: str, caption: str
    ) -> int | None:
        bot = await get_bot()
        msg_id = None
        if media_type == "docs":
            try:
                file = FSInputFile(media_path, filename=caption)
                res: Message = await bot.send_document(
                    chat_id=self.__settings.TG_CHANNEL_ID, document=file
                )
                msg_id = res.message_id
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to upload to Telegram: {str(e)}",
                )
        elif media_type == "video":
            try:
                file = FSInputFile(media_path, filename=caption)
                res: Message = await bot.send_video(
                    chat_id=self.__settings.TG_CHANNEL_ID, video=file, caption=caption
                )
                msg_id = res.message_id
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to upload to Telegram: {str(e)}",
                )
        elif media_type == "music":
            try:
                file = FSInputFile(media_path, filename=caption)
                res: Message = await bot.send_audio(
                    chat_id=self.__settings.TG_CHANNEL_ID, audio=file, caption=caption
                )
                msg_id = res.message_id
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to upload to Telegram: {str(e)}",
                )
        else:
            try:
                file = FSInputFile(media_path, filename=caption)
                res: Message = await bot.send_document(
                    chat_id=self.__settings.TG_CHANNEL_ID,
                    document=file,
                )
                msg_id = res.message_id
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to upload to Telegram: {str(e)}",
                )
        try:
            os.remove(media_path)
        except Exception as e:
            pass
        return msg_id

    async def _delete_from_telegram(self, message_id: int) -> None:
        bot = await get_bot()
        try:
            await bot.delete_message(
                chat_id=self.__settings.TG_CHANNEL_ID, message_id=message_id
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete from Telegram: {str(e)}",
            )

    async def post(
            self, /, *, payload: EntertainmentCreateSchema
    ) -> EntertainmentResponseSchema:
        if payload.type_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Type ID cannot be empty.",
            )
        await self._validate_entertainment_type(payload.type_id)
        message_id = await self._upload_to_telegram(
            media_path=payload.media_path,
            media_type=payload.media_type,
            caption=payload.title,
        )
        entertainment = await self.__entertainment_repo.post(
            payload, message_id=message_id
        )
        return EntertainmentResponseSchema.model_validate(entertainment)

    async def put(
            self, entertainment_id: int, payload: EntertainmentUpdate
    ) -> EntertainmentResponseSchema:
        await self._validate_entertainment_type(payload.type_id)
        entertainment = await self.__entertainment_repo.put(entertainment_id, payload)
        return EntertainmentResponseSchema.model_validate(entertainment)

    async def delete(self, entertainment_id: int) -> None:
        entertainment = await self.__entertainment_repo.get(entertainment_id)
        if not entertainment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entertainment not found",
            )
        await self.__entertainment_repo.delete(entertainment_id)
        await self._delete_from_telegram(entertainment.message_id)
        return None
