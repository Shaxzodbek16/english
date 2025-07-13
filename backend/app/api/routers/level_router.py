from fastapi import APIRouter, status, Depends

from app.api.utils.admin_filter import check_admin
from app.api.utils.jwt_handler import get_current_user
from app.api.controllers import LevelController
from app.api.schemas import (
    LevelResponseSchema,
    LevelCreateSchema,
    LevelUpdateSchema,
    LevelListResponseSchema,
    LevelQueryParamsSchema,
)

router = APIRouter(
    prefix="/level",
    tags=["Level"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="List all levels",
    response_model=LevelListResponseSchema,
)
async def list_(
    query: LevelQueryParamsSchema = Depends(),
    level_controller: LevelController = Depends(),
) -> LevelListResponseSchema:
    return await level_controller.list_(query=query)


@router.get(
    "/{level_id}",
    status_code=status.HTTP_200_OK,
    summary="Get a specific level by ID",
    response_model=LevelResponseSchema,
)
async def get(
    level_id: int, level_controller: LevelController = Depends()
) -> LevelResponseSchema:
    return await level_controller.get(level_id=level_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new level",
    description="Two types of levels are available: 'section', 'level' and 'theme'.",
    response_model=LevelResponseSchema,
    dependencies=[Depends(check_admin)],
)
async def post(
    payload: LevelCreateSchema, level_controller: LevelController = Depends()
) -> LevelResponseSchema:
    return await level_controller.post(payload=payload)


@router.put(
    "/{level_id}/",
    status_code=status.HTTP_200_OK,
    summary="Update an existing level",
    response_model=LevelResponseSchema,
    dependencies=[Depends(check_admin)],
)
async def put(
    level_id: int,
    payload: LevelUpdateSchema,
    level_controller: LevelController = Depends(),
) -> LevelResponseSchema:
    return await level_controller.put(level_id=level_id, payload=payload)


@router.delete(
    "/{level_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a level",
    response_model=None,
    dependencies=[Depends(check_admin)],
)
async def delete(level_id: int, level_controller: LevelController = Depends()) -> None:
    return await level_controller.delete(level_id=level_id)
