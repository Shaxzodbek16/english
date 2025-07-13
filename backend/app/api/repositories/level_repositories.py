from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from typing import Sequence

from app.api.controllers.media_controller import MediaController
from app.api.models import Level
from app.api.schemas import LevelCreateSchema, LevelUpdateSchema, LevelQueryParamsSchema
from app.core.databases.postgres import get_general_session


class LevelRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.__session = session

    async def list_(self, query: LevelQueryParamsSchema) -> Sequence[Level]:
        query_obj = select(Level).offset(query.offset).limit(query.limit)
        if not query.type and query.type not in ["section", "level", "theme"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid type. Must be one of 'section', 'level', or 'theme'.",
            )
        if query.type:
            query_obj = query_obj.where(Level.type == query.type)
        if query.search:
            query_obj = query_obj.where(Level.name.ilike(f"%{query.search}%"))
        if query.sort:
            sort_column = getattr(Level, query.sort.lstrip("-"), None)
            if sort_column:
                query_obj = query_obj.order_by(
                    sort_column.desc() if query.sort.startswith("-") else sort_column
                )
        if query.filter:
            filter_column = getattr(Level, query.filter.lstrip("-"), None)
            if filter_column:
                query_obj = query_obj.where(
                    filter_column.is_(
                        True if not query.filter.startswith("-") else False
                    )
                )
        result = await self.__session.execute(query_obj)
        return result.scalars().all()

    async def get(self, level_id: int) -> Level | None:
        level = await self.__session.execute(select(Level).where(Level.id == level_id))
        return level.scalar_one_or_none()

    async def post(self, payload: LevelCreateSchema) -> Level:
        level = Level(**payload.model_dump())
        try:
            self.__session.add(level)
            await self.__session.commit()
            return level
        except IntegrityError:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Level already exists with '{level.name}' name.",
            )
        except Exception as e:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while creating the level: {str(e)}",
            )

    async def put(self, level_id: int, payload: LevelUpdateSchema) -> Level:
        level = await self.get(level_id)
        if not level:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Level not found."
            )
        level.update(payload.model_dump(exclude_unset=True))
        try:
            self.__session.add(level)
            await self.__session.commit()
        except IntegrityError:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Level already exists with the same name.",
            )
        except Exception as e:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while updating the level: {str(e)}",
            )
        return level

    async def delete(self, level_id: int) -> None:
        level = await self.get(level_id)
        if not level:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Level not found."
            )
        await self.__session.delete(level)
        await self.__session.commit()
