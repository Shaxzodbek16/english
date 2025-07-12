from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode

from bot.app.handlers.user import UserRepository
from bot.core.databases.postgres import get_session

start_router = Router()


def phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Send phone number", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


@start_router.message(CommandStart())
async def handle_start(message: Message):
    await message.answer(
        "📲 To use this bot, you must share your phone number.",
        reply_markup=phone_keyboard(),
    )


@start_router.message(F.contact)
async def handle_contact(message: Message):
    contact = message.contact
    if contact.user_id != message.from_user.id:
        return await message.answer(
            "🚫 Please send your *own* phone number using the button.",
            parse_mode=ParseMode.HTML,
        )

    phone = contact.phone_number.lstrip("+").replace(" ", "")

    async for session in get_session():
        repo = UserRepository(session)

        user_data = {
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "telegram_id": message.from_user.id,
            "language": message.from_user.language_code or "en",
            "phone_number": int(phone),
        }
        await repo.create_if_not_exists(user_data)
        break

    await message.answer("✅ You have been successfully registered!", reply_markup=None)
    return None
