from typing import Sequence
from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from datetime import date

from app.api.schemas import UserAnswerQuery, UserAnswerCreateSchema
from app.core.databases.postgres import get_general_session
from app.api.models import UserAnswer


class UserAnswerRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.__session: AsyncSession = session

    async def list_(self, query: UserAnswerQuery, user_id: int) -> Sequence[UserAnswer]:
        stmt = select(UserAnswer).where(UserAnswer.user_id == user_id)
        if query.start_date:
            stmt = stmt.where(UserAnswer.created_at >= query.start_date)
        if query.end_date:
            stmt = stmt.where(UserAnswer.created_at <= query.end_date)
        stmt = stmt.offset(query.offset).limit(query.limit)
        result = await self.__session.execute(stmt)
        return result.scalars().all()

    async def get(self, user_answer_id: int) -> UserAnswer | None:
        stmt = select(UserAnswer).where(UserAnswer.id == user_answer_id)
        result = await self.__session.execute(stmt)
        return result.scalar_one_or_none()

    async def post(self, payload: UserAnswerCreateSchema, user_id: int) -> UserAnswer:
        user_answer = UserAnswer(**payload.model_dump(), user_id=user_id)
        try:
            self.__session.add(user_answer)
            await self.__session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User answer already exists for this user and question.",
            )
        except Exception as e:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while saving the user answer: {str(e)}",
            )
        await self.__session.refresh(user_answer)
        return user_answer

    async def get_correct_answers(
        self, user_id: int, start_date: date, end_date: date
    ) -> Sequence[UserAnswer]:
        stmt = select(UserAnswer).where(
            UserAnswer.user_id == user_id,
            UserAnswer.created_at >= start_date,
            UserAnswer.created_at <= end_date,
        )
        result = await self.__session.execute(stmt)
        return result.scalars().all()

    async def get_total_questions(self, user_id: int) -> int:
        stmt = (
            select(func.count())
            .select_from(UserAnswer)
            .where(UserAnswer.user_id == user_id)
        )
        result = await self.__session.execute(stmt)
        return result.scalar_one()

    async def get_option_by_question_id(
        self, question_id: int, user_id: int
    ) -> UserAnswer | None:
        stmt = select(UserAnswer).where(
            UserAnswer.question_id == question_id, UserAnswer.user_id == user_id
        )
        result = await self.__session.execute(stmt)
        return result.scalar_one_or_none()
