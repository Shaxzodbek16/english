from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from typing import Sequence

from app.api.models import Entertainment
from app.api.schemas import (
    EntertainmentUpdate,
    EntertainmentCreateSchema,
    EntertainmentQuerySchema,
)
from app.core.databases.postgres import get_general_session


class EntertainmentRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)) -> None:
        self.__session: AsyncSession = session

    async def list_(self, query: EntertainmentQuerySchema) -> Sequence[Entertainment]:
        query_obj = select(Entertainment)
        if query.filter is not None:
            query_obj = query_obj.where(Entertainment.type_id == query.filter)
        sort_string = query.sort
        if sort_string:
            if sort_string.startswith("-"):
                sort_column = getattr(Entertainment, sort_string[1:], None)
                if sort_column:
                    query_obj = query_obj.order_by(sort_column.desc())
            else:
                sort_column = getattr(Entertainment, sort_string, None)
                if sort_column:
                    query_obj = query_obj.order_by(sort_column)
        if query.search:
            query_obj = query_obj.where(Entertainment.title.ilike(f"%{query.search}%"))
        query_obj = query_obj.offset(query.offset).limit(query.limit)
        result = await self.__session.execute(query_obj)
        return result.scalars().all()

    async def get(self, entertainment_id: int) -> Entertainment | None:
        query = select(Entertainment).where(Entertainment.id == entertainment_id)
        result = await self.__session.execute(query)
        return result.scalar_one_or_none()

    async def _add_2_db(self, obj: Entertainment) -> None:
        self.__session.add(obj)
        try:
            await self.__session.commit()
        except IntegrityError:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Entertainment already exists",
            )
        except Exception as e:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def post(
        self, payload: EntertainmentCreateSchema, message_id: int
    ) -> Entertainment:
        entertainment = Entertainment(
            message_id=message_id, title=payload.title, type_id=payload.type_id
        )
        await self._add_2_db(entertainment)
        return entertainment

    async def put(
        self, entertainment_id: int, payload: EntertainmentUpdate
    ) -> Entertainment:
        entertainment = await self.get(entertainment_id)
        if not entertainment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Entertainment not found"
            )

        entertainment.update(payload.model_dump(exclude_unset=True))
        await self._add_2_db(entertainment)
        return entertainment

    async def delete(self, entertainment_id: int) -> None:
        entertainment = await self.get(entertainment_id)
        if not entertainment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Entertainment not found"
            )
        await self.__session.delete(entertainment)
        try:
            await self.__session.commit()
        except Exception as e:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
        return None
