from fastapi import APIRouter, status, Depends, Query


from app.api.controllers import OptionController
from app.api.utils.jwt_handler import get_current_user
from app.api.schemas import (
    OptionResponseSchema,
    OptionListResponseSchema,
    QueryParamsSchema,
    OptionCreateSchema,
    OptionUpdateSchema,
)

router = APIRouter(
    prefix="/options", tags=["Options"], dependencies=[Depends(get_current_user)]
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=OptionListResponseSchema,
)
async def list_(
    question_id: int | None = Query(default=None),
    query: QueryParamsSchema = Depends(),
    option_controller: OptionController = Depends(),
) -> OptionListResponseSchema:
    return await option_controller.list_(query, question_id)


@router.get(
    "/{option_id}",
    status_code=status.HTTP_200_OK,
    response_model=OptionResponseSchema,
)
async def get(
    option_id: int,
    option_controller: OptionController = Depends(),
) -> OptionResponseSchema:
    return await option_controller.get(option_id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=OptionResponseSchema,
)
async def post(
    payload: OptionCreateSchema,
    option_controller: OptionController = Depends(),
) -> OptionResponseSchema:
    return await option_controller.post(payload)


@router.put(
    "/{option_id}",
    status_code=status.HTTP_200_OK,
    response_model=OptionResponseSchema,
)
async def update(
    option_id: int,
    payload: OptionUpdateSchema,
    option_controller: OptionController = Depends(),
) -> OptionResponseSchema:
    return await option_controller.put(option_id, payload)


@router.delete(
    "/{option_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    option_id: int,
    option_controller: OptionController = Depends(),
) -> None:
    return await option_controller.delete(option_id)
