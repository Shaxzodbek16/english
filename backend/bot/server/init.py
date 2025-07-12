import asyncio

from aiogram import Bot
from aiogram.types import BotCommand
from datetime import datetime, UTC

from bot.app.handlers.user import UserRepository
from bot.core.databases.postgres import get_session
from bot.core.settings import get_settings, Settings

settings: Settings = get_settings()


async def set_default_commands(bot: Bot):
    now = datetime.now(UTC)
    quiz_date = f"{now.day}-{now.month}-{now.year}"

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Start bot"),
            BotCommand(command="lang", description="Change language"),
            BotCommand(command="quiz", description=f"Quiz for {quiz_date}"),
            BotCommand(command="help", description="Get help"),
        ]
    )


from aiogram.types import ReactionTypeEmoji


async def sender_function(bot: Bot, message: str):
    async for session in get_session():
        repo = UserRepository(session)
        admins = await repo.get_all_users()

        for admin in admins:
            if admin.is_admin:
                try:
                    sent_msg = await bot.send_message(admin.telegram_id, message)

                    try:
                        await bot.set_message_reaction(
                            chat_id=admin.telegram_id,
                            message_id=sent_msg.message_id,
                            reaction=[ReactionTypeEmoji(emoji="⚡")],
                        )
                    except Exception as reaction_error:
                        print(f"❌ Failed to send reaction: {reaction_error}")

                    await asyncio.sleep(0.3)
                except Exception as e:
                    print(f"❌ Failed to send message to {admin.telegram_id}: {e}")
        break


async def send_message_to_admins(bot: Bot, message: str):
    await sender_function(bot, message)
