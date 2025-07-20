from typing import Sequence

from fastapi import Depends, HTTPException, status

from app.api.models import Question
from app.api.repositories import QuestionRepository, OptionRepository, LevelRepository
from app.api.schemas import (
    QuestionListResponseSchema,
    QuestionQueryParamSchema,
    QuestionResponseSchema,
    QuestionCreateSchema,
    QuestionUpdateSchema,
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

    async def _validate_level_and_theme(
        self, level_id: int, theme_id: int, update: bool = False
    ) -> None:
        if update:
            if level_id:
                level = await self.__level_repository.get(level_id)
                if not level:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Level with ID {level_id} not found.",
                    )
                elif level.type != "level":
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"It is not level id {level_id} for questions.",
                    )
            if theme_id:
                theme = await self.__level_repository.get(theme_id)
                if not theme:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Theme with ID {theme_id} not found.",
                    )
                elif theme.type != "theme":
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"It is not theme id {theme_id} for questions.",
                    )
            return
        level = await self.__level_repository.get(level_id)
        theme = await self.__level_repository.get(theme_id)
        if not level:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Level with ID {level_id} not found.",
            )
        if not theme:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Theme with ID {theme_id} not found.",
            )
        if level.type != "level":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"It is not level id {level_id} for questions.",
            )
        if theme.type != "theme":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"It is not theme id {theme_id} for questions.",
            )

    async def _response_to_list(
        self, questions: Sequence[Question], query: QuestionQueryParamSchema
    ) -> QuestionListResponseSchema:
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

    async def list_(
        self,
        query: QuestionQueryParamSchema,
    ) -> QuestionListResponseSchema:
        if query.level_id is not None:
            level = await self.__level_repository.get(query.level_id)
            if not level:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Level with ID {query.level_id} not found.",
                )
        if query.theme_id is not None:
            theme = await self.__level_repository.get(query.theme_id)
            if not theme:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Theme with ID {query.theme_id} not found.",
                )
        questions = await self.__question_repository.list_(query=query)
        if not questions:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="No questions found.",
            )
        return await self._response_to_list(questions, query)

    async def get(self, question_id: int) -> QuestionResponseSchema:
        question = await self.__question_repository.get(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID {question_id} not found.",
            )
        options = await self.__option_repository.get_question_options(question_id)
        return QuestionResponseSchema(
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
                OptionResponseSchema.model_validate(option) for option in options
            ],
        )

    async def _response_to_question(self, question: Question) -> QuestionResponseSchema:
        return QuestionResponseSchema(
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

    async def post(self, payload: QuestionCreateSchema) -> QuestionResponseSchema:
        if not payload.level_id or not payload.theme_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Level ID and Theme ID are required.",
            )
        await self._validate_level_and_theme(payload.level_id, payload.theme_id)
        question = await self.__question_repository.post(payload)
        return await self._response_to_question(question)

    async def put(
        self, question_id: int, payload: QuestionUpdateSchema
    ) -> QuestionResponseSchema:
        question = await self.__question_repository.get(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID {question_id} not found.",
            )
        await self._validate_level_and_theme(
            payload.level_id, payload.theme_id, update=True
        )
        updated_question = await self.__question_repository.put(question_id, payload)
        return await self._response_to_question(updated_question)

    async def delete(self, question_id: int) -> None:
        question = await self.__question_repository.get(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with ID {question_id} not found.",
            )
        await self.__question_repository.delete(question_id)
        return None

    async def random(
        self, level_id: int, theme_id: int, limit
    ) -> list[QuestionResponseSchema]:
        await self._validate_level_and_theme(level_id, theme_id)
        questions = await self.__question_repository.random(level_id, theme_id, limit)
        return (
            [await self._response_to_question(question) for question in questions]
            if questions
            else []
        )
