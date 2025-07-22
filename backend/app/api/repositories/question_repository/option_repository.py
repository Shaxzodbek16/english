from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException, status
from typing import Sequence

from app.api.models import Option
from app.api.schemas import QueryParamsSchema, OptionCreateSchema, OptionUpdateSchema
from app.core.databases.postgres import get_general_session


class OptionRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.__session = session

    async def list_(
        self, query: QueryParamsSchema, question_id: int | None
    ) -> Sequence[Option]:
        query_obj = select(Option)
        if question_id is not None:
            query_obj = select(Option).where(Option.question_id == question_id)
        if query.search:
            query_obj = query_obj.where(Option.option.ilike(f"%{query.search}%"))
        if query.sort:
            if query.sort.startswith("-"):
                query_obj = query_obj.order_by(getattr(Option, query.sort[1:]).desc())
            else:
                query_obj = query_obj.order_by(getattr(Option, query.sort).asc())
        if query.filter:
            if query.filter == "is_correct":
                query_obj = query_obj.where(Option.is_correct.is_(True))
            if query.filter == "-is_correct":
                query_obj = query_obj.where(Option.is_correct.is_(False))
        query_obj = query_obj.offset(query.offset).limit(query.limit)
        result = await self.__session.execute(query_obj)
        return result.scalars().all()

    async def get(self, option_id: int) -> Option | None:
        query_obj = select(Option).where(Option.id == option_id)
        result = await self.__session.execute(query_obj)
        return result.scalar_one_or_none()

    async def get_question_options(self, question_id: int) -> Sequence[Option]:
        query_obj = select(Option).where(Option.question_id == question_id)
        result = await self.__session.execute(query_obj)
        return result.scalars().all()

    async def _add_2_db(self, obj: Option) -> None:
        self.__session.add(obj)
        try:
            await self.__session.commit()
        except IntegrityError:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Option with this name already exists for this question.",
            )
        except Exception as e:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    async def post(self, payload: OptionCreateSchema) -> Option:
        option = Option(**payload.model_dump())
        await self._add_2_db(option)
        return option

    async def put(self, option_id: int, payload: OptionUpdateSchema) -> Option:
        option = await self.get(option_id)
        if not option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Option not found.",
            )
        option.update(payload.model_dump(exclude_unset=True))
        await self._add_2_db(option)
        return option

    async def delete(self, option_id: int) -> None:
        option = await self.get(option_id)
        if not option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Option not found."
            )
        await self.__session.delete(option)
        try:
            await self.__session.commit()
            return None
        except Exception as e:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

    async def check_answer(self, question_id: int, option_id: int) -> bool:
        stmt = select(Option).where(
            Option.question_id == question_id, Option.id == option_id
        )
        result = await self.__session.execute(stmt)
        option = result.scalar_one_or_none()
        if option is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Option not found for the given question.",
            )
        return option.is_correct
