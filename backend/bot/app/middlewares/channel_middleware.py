from typing import Callable, Awaitable, Dict, Any, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from bot.app.handlers.channel import ChannelRepository
from bot.app.handlers.user import UserRepository
from bot.core.databases.postgres import get_session
from bot.app.keyboards.channel_sub import get_channel_keyboard


class CheckSubscriptionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any],
    ) -> Any:
        bot = data["bot"]
        user_id = event.from_user.id
        admins_id = []
        async for session in get_session():
            user_repo = UserRepository(session)
            admins = await user_repo.get_admins()
            admins_id = {admin.telegram_id for admin in admins}
        if user_id in admins_id: return await handler(event, data)
        if isinstance(event, Message):
            text = event.text or ""
            if text.startswith("/help") or text.startswith("/start"):
                return await handler(event, data)
            unsubscribed = []
            async for session in get_session():
                repo = ChannelRepository(session)
                unsubscribed = await repo.fetch_unsubscribed_channels(user_id, bot)
                break
            if unsubscribed:
                buttons = await get_channel_keyboard(unsubscribed)
                prompt = f"📢 Please subscribe to the following {len(unsubscribed)} channels first:"
                try:
                    await event.answer(text=prompt, reply_markup=buttons)
                except TelegramBadRequest as e:
                    if "message is not modified" not in str(e):
                        raise
                return None

        return await handler(event, data)
