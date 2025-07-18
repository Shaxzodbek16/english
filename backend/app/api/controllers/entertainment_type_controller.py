from fastapi import Depends, HTTPException, status

from app.api.repositories import EntertainmentTypeRepository
from app.api.schemas import EntertainmentTypesSchema, EntertainmentTypesResponseSchema


class EntertainmentTypeController:
    def __init__(
        self, entertainment_type_repo: EntertainmentTypeRepository = Depends()
    ):
        self.__entertainment_type_repo = entertainment_type_repo

    async def get(self, entertainment_type_id: int) -> EntertainmentTypesResponseSchema:
        entertainment_type = await self.__entertainment_type_repo.get(
            entertainment_type_id
        )
        if not entertainment_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entertainment type not found",
            )
        return EntertainmentTypesResponseSchema.model_validate(entertainment_type)

    async def list(self) -> list[EntertainmentTypesResponseSchema]:
        entertainment_types = await self.__entertainment_type_repo.list_()
        if not entertainment_types:
            raise HTTPException(
                status_code=status.HTTP_200_OK,
                detail="No entertainment types found",
            )
        return [
            EntertainmentTypesResponseSchema.model_validate(entertainment_type)
            for entertainment_type in entertainment_types
        ]

    async def post(
        self, entertainment_type: EntertainmentTypesSchema
    ) -> EntertainmentTypesResponseSchema:
        created_entertainment_type = await self.__entertainment_type_repo.post(
            entertainment_type
        )
        return EntertainmentTypesResponseSchema.model_validate(
            created_entertainment_type
        )

    async def put(
        self, entertainment_type_id: int, entertainment_type: EntertainmentTypesSchema
    ) -> EntertainmentTypesResponseSchema:
        updated_entertainment_type = await self.__entertainment_type_repo.put(
            entertainment_type_id, entertainment_type
        )
        return EntertainmentTypesResponseSchema.model_validate(
            updated_entertainment_type
        )

    async def delete(self, entertainment_type_id: int) -> None:
        await self.__entertainment_type_repo.delete(entertainment_type_id)
        return None
