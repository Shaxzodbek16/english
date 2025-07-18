from typing import Sequence

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from app.api.models import EntertainmentTypes
from app.api.schemas import EntertainmentTypesSchema
from app.core.databases.postgres import get_general_session


class EntertainmentTypeRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)) -> None:
        self.__session: AsyncSession = session

    async def list_(self) -> Sequence[EntertainmentTypes]:
        query = select(EntertainmentTypes)
        result = await self.__session.execute(query)
        return result.scalars().all()

    async def get(self, type_id: int) -> EntertainmentTypes | None:
        query = select(EntertainmentTypes).where(EntertainmentTypes.id == type_id)
        result = await self.__session.execute(query)
        entertainment_type = result.scalar_one_or_none()

        return entertainment_type

    async def _add_2_db(self, obj: EntertainmentTypes) -> None:
        self.__session.add(obj)
        try:
            await self.__session.commit()
        except IntegrityError:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Entertainment type already exists",
            )
        except Exception as e:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def post(self, payload: EntertainmentTypesSchema) -> EntertainmentTypes:
        entertainment_type = EntertainmentTypes(**payload.model_dump())
        await self._add_2_db(entertainment_type)
        return entertainment_type

    async def put(
        self, entertainment_type_id: int, payload: EntertainmentTypesSchema
    ) -> EntertainmentTypes:
        entertainment_type = await self.get(entertainment_type_id)
        if not entertainment_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entertainment type not found",
            )

        entertainment_type.update(payload.model_dump(exclude_unset=True))
        await self._add_2_db(entertainment_type)
        return entertainment_type

    async def delete(self, entertainment_type_id: int) -> None:
        entertainment_type = await self.get(entertainment_type_id)
        if not entertainment_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entertainment type not found",
            )

        await self.__session.delete(entertainment_type)
        try:
            await self.__session.commit()
        except Exception as e:
            await self.__session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
        return None
