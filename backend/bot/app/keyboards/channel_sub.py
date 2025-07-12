from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.api.models import Channel


async def get_channel_keyboard(not_joined: list[Channel]):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"📢 {ch.name}", url=ch.link)]
            for ch in not_joined
        ]
        + [[InlineKeyboardButton(text="✅ Check", callback_data="check_subscription")]]
    )
