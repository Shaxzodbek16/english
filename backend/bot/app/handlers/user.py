from typing import Sequence
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_admins(self) -> Sequence[User]:
        stmt = select(User).where(User.is_admin == True)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_if_not_exists(self, user_data: dict) -> User:
        user = await self.get_by_telegram_id(user_data["telegram_id"])
        if user:
            return user

        user = User(**user_data)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_by_telegram_id(
        self, telegram_id: int, update_data: dict
    ) -> User | None:
        user = await self.get_by_telegram_id(telegram_id)
        if not user:
            return None

        user.update(update_data)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_by_telegram_id(self, telegram_id: int) -> bool:
        stmt = delete(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0  # noqa

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> Sequence[User]:
        stmt = select(User).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
