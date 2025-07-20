from fastapi import Depends, HTTPException, status

from app.api.repositories import OptionRepository, QuestionRepository
from app.api.schemas import (
    QueryParamsSchema,
    OptionResponseSchema,
    OptionCreateSchema,
    OptionUpdateSchema,
    OptionListResponseSchema,
)


class OptionController:
    def __init__(
        self,
        option_repository: OptionRepository = Depends(),
        question_repository: QuestionRepository = Depends(),
    ):
        self.__option_repository = option_repository
        self.__question_repository = question_repository

    async def list_(
        self, query: QueryParamsSchema, question_id: int | None = None
    ) -> OptionListResponseSchema:
        if question_id is not None:
            question = await self.__question_repository.get(question_id)
            if not question:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Question with id {question_id} not found",
                )
        options = await self.__option_repository.list_(query, question_id)
        if not options:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="No options found",
            )
        return OptionListResponseSchema(
            page=query.page,
            size=query.size,
            search=query.search,
            filter=query.filter,
            sort=query.sort,
            total=len(options),
            items=[OptionResponseSchema.model_validate(option) for option in options],
        )

    async def get(self, option_id: int) -> OptionResponseSchema:
        option = await self.__option_repository.get(option_id)
        if not option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Option with id {option_id} not found",
            )
        return OptionResponseSchema.model_validate(option)

    async def post(self, payload: OptionCreateSchema) -> OptionResponseSchema:
        option = await self.__option_repository.post(payload)
        return OptionResponseSchema.model_validate(option)

    async def put(
        self, option_id: int, payload: OptionUpdateSchema
    ) -> OptionResponseSchema:
        option = await self.__option_repository.put(
            option_id,
            payload,
        )
        if not option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Option with id {option_id} not found",
            )
        return OptionResponseSchema.model_validate(option)

    async def delete(self, option_id: int) -> None:
        option = await self.__option_repository.get(option_id)
        if not option:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Option with id {option_id} not found",
            )
        return await self.__option_repository.delete(option_id)
