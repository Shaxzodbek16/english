from typing import Sequence
from fastapi import Depends, HTTPException, status

from app.api.models import Level
from app.api.repositories import LevelRepository
from app.api.schemas import (
    LevelListResponseSchema,
    LevelCreateSchema,
    LevelResponseSchema,
    LevelUpdateSchema,
    LevelQueryParamsSchema,
)


class LevelController:
    def __init__(self, level_repository: LevelRepository = Depends()):
        self.__level_repository: LevelRepository = level_repository

    async def list_(self, query: LevelQueryParamsSchema) -> LevelListResponseSchema:
        levels: Sequence[Level] = await self.__level_repository.list_(query=query)
        if levels:
            return LevelListResponseSchema(
                page=query.page,
                size=query.size,
                search=query.search,
                sort=query.sort,
                filter=query.filter,
                total=len(levels),
                items=[LevelResponseSchema.model_validate(level) for level in levels],
            )
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="We have not found any levels",
        )

    async def get(self, level_id: int) -> LevelResponseSchema:
        level: Level | None = await self.__level_repository.get(level_id=level_id)
        if not level:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Level not found",
            )
        return LevelResponseSchema.model_validate(level)

    async def post(self, payload: LevelCreateSchema) -> LevelResponseSchema:
        level: Level = await self.__level_repository.post(payload=payload)
        return LevelResponseSchema.model_validate(level)

    async def put(
        self, level_id: int, payload: LevelUpdateSchema
    ) -> LevelResponseSchema:
        level: Level = await self.__level_repository.put(
            level_id=level_id, payload=payload
        )
        return LevelResponseSchema.model_validate(level)

    async def delete(self, level_id: int) -> None:
        return await self.__level_repository.delete(level_id=level_id)
