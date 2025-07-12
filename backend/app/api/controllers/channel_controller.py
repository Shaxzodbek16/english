from typing import Sequence

from fastapi import Depends, HTTPException, status

from app.api.models import User, Channel
from app.api.repositories import ChannelRepository
from app.api.schemas import (
    QueryParamsSchema,
    ChannelListResponseSchema,
    ChannelResponseSchema,
    UpdateChannelSchema,
    CreateChannelSchema,
)


class ChannelController:
    def __init__(self, channel_repo: ChannelRepository = Depends()):
        self.__channel_repo: ChannelRepository = channel_repo

    @staticmethod
    async def check_admin(user: User):
        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Page not found",
            )

    async def list(self, /, *, params: QueryParamsSchema) -> ChannelListResponseSchema:
        channels: Sequence[Channel] = await self.__channel_repo.list(params)
        if channels:
            return ChannelListResponseSchema(
                page=params.page,
                size=params.size,
                search=params.search,
                sort=params.sort,
                filter=params.filter,
                total=len(channels),
                items=[
                    ChannelResponseSchema.model_validate(channel)
                    for channel in channels
                ],
            )
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="We have not found any channels",
        )

    async def get(self, /, *, channel_id: int) -> ChannelResponseSchema:
        channel: Channel | None = await self.__channel_repo.get(channel_id)
        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found",
            )
        return ChannelResponseSchema.model_validate(channel)

    async def post(self, /, *, payload: CreateChannelSchema) -> ChannelResponseSchema:
        payload.channel_id = payload.channel_id * -1
        channel = await self.__channel_repo.post(payload)
        return ChannelResponseSchema.model_validate(channel)

    async def put(
        self, /, *, channel_id: int, payload: UpdateChannelSchema
    ) -> ChannelResponseSchema:
        payload.channel_id = payload.channel_id * -1
        channel = await self.__channel_repo.put(channel_id, payload)
        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found",
            )
        return ChannelResponseSchema.model_validate(channel)

    async def delete(self, /, *, channel_id: int) -> None:
        return await self.__channel_repo.delete(channel_id)
