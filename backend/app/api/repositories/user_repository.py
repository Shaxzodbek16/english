from typing import Sequence
from sqlalchemy import or_, asc, desc, String
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.models import User
from app.api.schemas import QueryParamsSchema, UserUpdateSchema
from app.core.databases.postgres import get_general_session


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)) -> None:
        self.__session = session

    async def get(self, phone_number: int) -> User | None:
        user = await self.__session.execute(
            select(User).where(User.phone_number == phone_number)
        )
        return user.scalar_one_or_none()

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        user = await self.__session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return user.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        user = await self.__session.execute(select(User).where(User.id == user_id))
        return user.scalar_one_or_none()

    async def list(self, params: QueryParamsSchema) -> Sequence[User]:
        stmt = select(User)
        if params.filter:
            field = params.filter
            if field == "is_admin":
                stmt = stmt.where(User.is_admin.is_(True))
            if field == "-is_admin":
                stmt = stmt.where(User.is_admin.is_(False))
            elif field == "language":
                stmt = stmt.where(User.language != None)

        if params.search:
            stmt = stmt.where(
                or_(
                    User.first_name.ilike(f"%{params.search}%"),
                    User.last_name.ilike(f"%{params.search}%"),
                    User.phone_number.cast(String).ilike(f"%{params.search}%"),
                    User.telegram_id.cast(String).ilike(f"%{params.search}%"),
                )
            )
        if params.sort:
            sort_field = params.sort.lstrip("-")
            sort_column = getattr(User, sort_field, None)
            if sort_column is not None:
                order = asc if not params.sort.startswith("-") else desc
                stmt = stmt.order_by(order(sort_column))
        stmt = stmt.offset(params.offset).limit(params.limit)

        result = await self.__session.execute(stmt)
        return result.scalars().all()

    async def update(self, phone_number: int, payload: UserUpdateSchema) -> User:
        user = await self.get(phone_number)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        user.update(payload.model_dump(exclude_unset=True))

        self.__session.add(user)
        await self.__session.commit()
        await self.__session.refresh(user)
        return user
