from fastapi import Depends, status, HTTPException
from datetime import date

from app.api.models import User
from app.api.repositories import (
    UserAnswerRepository,
    QuestionRepository,
    UserRepository,
    OptionRepository,
)
from app.api.schemas import (
    UserAnswerQuery,
    UserAnswerListResponseSchema,
    UserAnswerResponseSchema,
    UserAnswerCreateSchema,
)


class UserAnswerController:
    def __init__(
        self,
        user_answer_repository: UserAnswerRepository = Depends(),
        user_repository: UserRepository = Depends(),
        question_repository: QuestionRepository = Depends(),
        option_repository: OptionRepository = Depends(),
    ):
        self.__user_answer_repository: UserAnswerRepository = user_answer_repository
        self.__user_repository: UserRepository = user_repository
        self.__question_repository: QuestionRepository = question_repository
        self.__option_repository: OptionRepository = option_repository

    async def list_(
        self, query: UserAnswerQuery, user_id: int
    ) -> UserAnswerListResponseSchema:
        user: User | None = await self.__user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                detail="User not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        if query.start_date is None:
            query.start_date = date.today()
        if query.end_date is None:
            query.end_date = user.get_created_time
        user_answers = await self.__user_answer_repository.list_(
            query=query, user_id=user_id
        )
        if not user_answers:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="No user answers found for the given query.",
            )

        correct_answers = await self.get_correct_answers(
            user_id, start_date=query.start_date, end_date=query.end_date
        )
        total_questions = await self.__user_answer_repository.get_total_questions(
            user_id
        )
        return UserAnswerListResponseSchema(
            page=query.page,
            size=query.size,
            total=len(user_answers),
            start_date=query.start_date,
            end_date=query.end_date,
            correct_answers=correct_answers,
            total_questions=total_questions,
            accuracy=(correct_answers / total_questions) * 100,
            user_answers=[
                UserAnswerResponseSchema.model_validate(user_answer)
                for user_answer in user_answers
            ],
        )

    async def get_correct_answers(
        self, user_id: int, start_date: date, end_date: date
    ) -> int:
        user_answers = await self.__user_answer_repository.get_correct_answers(
            user_id, start_date, end_date
        )
        counter = 0
        for user_answer in user_answers:
            if await self.__option_repository.check_answer(
                user_answer.question_id, user_answer.option_id
            ):
                counter += 1
        return counter

    async def _validate_data(self, user_answer: UserAnswerCreateSchema) -> None:
        question = await self.__question_repository.get(user_answer.question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Question not found",
            )
        option = await self.__option_repository.get(user_answer.option_id)
        if not option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Option not found",
            )
        if option.question_id != question.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Option does not belong to the specified question",
            )

    async def post(
        self, payload: UserAnswerCreateSchema, user_id: int
    ) -> UserAnswerResponseSchema:
        await self._validate_data(payload)
        user_answer = await self.__user_answer_repository.post(
            payload=payload, user_id=user_id
        )
        return UserAnswerResponseSchema.model_validate(user_answer)
