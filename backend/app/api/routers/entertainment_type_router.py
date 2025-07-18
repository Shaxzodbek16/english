from fastapi import Depends, APIRouter, status

from app.api.controllers import EntertainmentTypeController
from app.api.schemas import EntertainmentTypesSchema, EntertainmentTypesResponseSchema

router = APIRouter(
    prefix="/entertainment-type",
    tags=["Entertainment Type"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[EntertainmentTypesResponseSchema],
)
async def list_(
    entertainment_type_controller: EntertainmentTypeController = Depends(),
) -> list[EntertainmentTypesResponseSchema]:
    return await entertainment_type_controller.list()


@router.get(
    "/{entertainment_type_id}",
    status_code=status.HTTP_200_OK,
    response_model=EntertainmentTypesResponseSchema,
)
async def get(
    entertainment_type_id: int,
    entertainment_type_controller: EntertainmentTypeController = Depends(),
) -> EntertainmentTypesResponseSchema:
    return await entertainment_type_controller.get(entertainment_type_id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=EntertainmentTypesResponseSchema,
)
async def post(
    entertainment_type: EntertainmentTypesSchema,
    entertainment_type_controller: EntertainmentTypeController = Depends(),
) -> EntertainmentTypesResponseSchema:
    return await entertainment_type_controller.post(entertainment_type)


@router.put(
    "/{entertainment_type_id}",
    status_code=status.HTTP_200_OK,
    response_model=EntertainmentTypesResponseSchema,
)
async def put(
    entertainment_type_id: int,
    entertainment_type: EntertainmentTypesSchema,
    entertainment_type_controller: EntertainmentTypeController = Depends(),
) -> EntertainmentTypesResponseSchema:
    return await entertainment_type_controller.put(
        entertainment_type_id, entertainment_type
    )


@router.delete("/{entertainment_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    entertainment_type_id: int,
    entertainment_type_controller: EntertainmentTypeController = Depends(),
) -> None:
    return await entertainment_type_controller.delete(entertainment_type_id)
