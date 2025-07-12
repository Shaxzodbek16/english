from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from bot.app.handlers.channel import ChannelRepository
from bot.app.keyboards.channel_sub import get_channel_keyboard
from bot.core.databases.postgres import get_session

channel_router = Router()




@channel_router.callback_query(F.data == "check_subscription")
async def handle_check_subscription(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    bot = callback_query.bot
    unsubscribed = []

    async for session in get_session():
        repo = ChannelRepository(session)

        unsubscribed = await repo.fetch_unsubscribed_channels(user_id, bot)
        break

    if unsubscribed:
        kb = await get_channel_keyboard(unsubscribed)
        try:
            await callback_query.message.edit_text(
                text="🚫 You still need to join these channels.", reply_markup=kb
            )
        except TelegramBadRequest as e:
            if "message is not modified" not in str(e):
                raise
    else:
        try:
            await callback_query.message.delete()
        except TelegramBadRequest as e:
            pass
        await callback_query.message.answer("start")
