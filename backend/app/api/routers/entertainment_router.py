from fastapi import Depends, APIRouter, status

from app.api.controllers import EntertainmentController
from app.api.schemas import (
    EntertainmentListResponseSchema,
    EntertainmentResponseSchema,
    EntertainmentCreateSchema,
    EntertainmentUpdate,
    EntertainmentQuerySchema,
)
from app.api.utils.admin_filter import check_admin
from app.api.utils.jwt_handler import get_current_user

router = APIRouter(
    prefix="/entertainment",
    tags=["Entertainment"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=EntertainmentListResponseSchema
)
async def list_(
    query: EntertainmentQuerySchema = Depends(),
    entertainment_controller: EntertainmentController = Depends(),
) -> EntertainmentListResponseSchema:
    return await entertainment_controller.list_(query)


@router.get(
    "/{entertainment_id}",
    status_code=status.HTTP_200_OK,
    response_model=EntertainmentResponseSchema,
)
async def get(
    entertainment_id: int, entertainment_controller: EntertainmentController = Depends()
) -> EntertainmentResponseSchema:
    return await entertainment_controller.get(entertainment_id)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=EntertainmentResponseSchema
)
async def post(
    payload: EntertainmentCreateSchema,
    entertainment_controller: EntertainmentController = Depends(),
) -> EntertainmentResponseSchema:
    return await entertainment_controller.post(payload=payload)


@router.put(
    "/{entertainment_id}",
    status_code=status.HTTP_200_OK,
    response_model=EntertainmentResponseSchema,
)
async def update(
    entertainment_id: int,
    entertainment: EntertainmentUpdate,
    entertainment_controller: EntertainmentController = Depends(),
) -> EntertainmentResponseSchema:
    return await entertainment_controller.put(entertainment_id, entertainment)


@router.delete("/{entertainment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    entertainment_id: int, entertainment_controller: EntertainmentController = Depends()
) -> None:
    return await entertainment_controller.delete(entertainment_id)
