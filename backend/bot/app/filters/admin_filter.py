from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.core.databases.postgres import get_session
from bot.app.handlers.user import UserRepository


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        async for session in get_session():
            repo = UserRepository(session)
            user = await repo.get_by_telegram_id(message.from_user.id)
            return bool(user and user.is_admin)
        return False
