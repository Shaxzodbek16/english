from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.models import User
from app.core.databases.postgres import get_general_session


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)) -> None:
        self.__session = session

    async def get(self, phone_number: int) -> User | None:
        user = await self.__session.execute(
            select(User).where(User.phone_number == phone_number)
        )
        return user.scalar_one_or_none()
