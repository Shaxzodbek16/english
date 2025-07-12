from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from typing import Sequence

from app.api.models import Channel
from app.api.schemas import QueryParamsSchema, CreateChannelSchema, UpdateChannelSchema
from app.core.databases.postgres import get_general_session


class ChannelRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)) -> None:
        self.__session: AsyncSession = session

    async def list(self, params: QueryParamsSchema) -> Sequence[Channel]:
        query = select(Channel).offset(params.offset).limit(params.limit)
        if params.search:
            query = query.where(Channel.name.ilike(f"%{params.search}%"))
        if params.sort:
            sort_column = getattr(Channel, params.sort.lstrip("-"), None)
            if sort_column:
                query = query.order_by(
                    sort_column.desc() if params.sort.startswith("-") else sort_column
                )
        if params.filter:
            filter_column = getattr(Channel, params.filter.lstrip("-"), None)
            if filter_column:
                query = query.where(
                    filter_column.is_(
                        True if not params.filter.startswith("-") else False
                    )
                )
        result = await self.__session.execute(query)
        return result.scalars().all()

    async def get(self, channel_id: int) -> Channel | None:
        query = select(Channel).where(Channel.id == channel_id)
        result = await self.__session.execute(query)
        return result.scalar_one_or_none()

    async def post(self, payload: CreateChannelSchema) -> Channel:
        channel = Channel(**payload.model_dump())
        try:
            self.__session.add(channel)
            await self.__session.commit()
            return await self.get(channel.channel_id)
        except IntegrityError:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Channel already exists",
            )

        except Exception:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the channel",
            )

    async def put(self, channel_id: int, payload: UpdateChannelSchema) -> Channel:
        channel = await self.get(channel_id)
        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found",
            )
        channel.update(payload.model_dump(exclude_unset=True))
        try:
            self.__session.add(channel)
            await self.__session.commit()
            return channel
        except IntegrityError:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Channel with {payload.channel_id} channel id already exists",
            )
        except Exception:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the channel",
            )

    async def delete(self, channel_id: int) -> None:
        channel = await self.get(channel_id)
        if not channel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found",
            )
        try:
            await self.__session.delete(channel)
            await self.__session.commit()
        except Exception:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while deleting the channel",
            )
