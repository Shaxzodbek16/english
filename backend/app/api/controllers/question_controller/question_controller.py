from fastapi import Depends, HTTPException, status

from app.api.repositories import QuestionRepository, OptionRepository, LevelRepository
from app.api.schemas import (
    QuestionListResponseSchema,
    QueryParamsSchema,
    QuestionResponseSchema,
)
from app.api.schemas.question_schema import OptionResponseSchema


class QuestionController:
    def __init__(
        self,
        question_repository: QuestionRepository = Depends(),
        option_repository: OptionRepository = Depends(),
        level_repository: LevelRepository = Depends(),
    ):
        self.__question_repository = question_repository
        self.__option_repository = option_repository
        self.__level_repository = level_repository

    async def list_(
        self,
        query: QueryParamsSchema,
    ) -> QuestionListResponseSchema:
        questions = await self.__question_repository.list_(query=query)
        if not questions:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="No questions found.",
            )
        return QuestionListResponseSchema(
            page=query.page,
            size=query.size,
            search=query.search,
            filter=query.filter,
            sort=query.sort,
            total=len(questions),
            items=[
                QuestionResponseSchema(
                    id=question.id,
                    name=question.name,
                    picture=question.picture,
                    answer=question.answer,
                    type=question.type,
                    level_id=question.level_id,
                    theme_id=question.theme_id,
                    created_at=question.created_at,
                    updated_at=question.updated_at,
                    variants=[
                        OptionResponseSchema.model_validate(option)
                        for option in await self.__option_repository.get_question_options(
                            question.id
                        )
                    ],
                )
                for question in questions
            ],
        )
