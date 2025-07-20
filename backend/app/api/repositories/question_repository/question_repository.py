from typing import Sequence
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException, status

from app.api.models import Question
from app.api.schemas import (
    QuestionCreateSchema,
    QuestionUpdateSchema,
    QueryParamsSchema,
)
from app.core.databases.postgres import get_general_session


class QuestionRepository:
    def __init__(
        self,
        session: AsyncSession = Depends(get_general_session),
    ):
        self.__session = session

    async def list_(
        self,
        query: QueryParamsSchema,
    ) -> Sequence[Question]:
        query_obj = select(Question)
        if query.search:
            query_obj = query_obj.where(Question.name.ilike(f"%{query.search}%"))
        if query.sort:
            if hasattr(Question, query.sort) or hasattr(Question, query.sort[1:]):
                if query.sort.startswith("-"):
                    query_obj = query_obj.order_by(
                        getattr(Question, query.sort[1:]).desc()
                    )
                else:
                    query_obj = query_obj.order_by(getattr(Question, query.sort).asc())
        if query.filter:
            if query.filter.startswith("-"):
                query_obj = query_obj.where(
                    getattr(
                        Question,
                        query.filter[1:],
                    ).is_(False)
                )
            else:
                query_obj = query_obj.where(
                    getattr(
                        Question,
                        query.filter,
                    ).is_(True)
                )
        query_obj = query_obj.offset(query.offset).limit(query.limit)
        questions = await self.__session.execute(query_obj)
        return questions.scalars().all()

    async def get(
        self,
        question_id: int,
    ) -> Question | None:
        query_obj = select(Question).where(Question.id == question_id)
        result = await self.__session.execute(query_obj)
        return result.scalar_one_or_none()

    async def add_2_db(
        self,
        question: Question,
    ) -> Question:
        self.__session.add(question)
        try:
            await self.__session.commit()
        except IntegrityError:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question already exists.",
            )
        except Exception as e:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while adding the question: {str(e)}",
            )
        await self.__session.refresh(question)
        return question

    async def post(
        self,
        payload: QuestionCreateSchema,
    ) -> Question:
        return await self.add_2_db(Question(**payload.model_dump()))

    async def put(
        self,
        question_id: int,
        payload: QuestionUpdateSchema,
    ) -> Question:
        question = await self.get(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found.",
            )
        question.update(
            **payload.model_dump(
                exclude_unset=True,
                exclude_none=True,
            )
        )
        return await self.add_2_db(question)

    async def delete(
        self,
        question_id: int,
    ) -> None:
        question = await self.get(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found.",
            )
        await self.__session.delete(question)
        try:
            await self.__session.commit()
        except Exception as e:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while deleting the question: {str(e)}",
            )
