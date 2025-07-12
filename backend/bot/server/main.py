import asyncio, logging, sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from datetime import datetime, UTC, timedelta

from bot.app.routers import main_router
from bot.core.settings import get_settings
from bot.server.init import set_default_commands, sender_function
from bot.app.middlewares.channel_middleware import CheckSubscriptionMiddleware


async def main() -> None:
    settings = get_settings()
    bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    await set_default_commands(bot)
    dp = Dispatcher()
    dp.message.middleware(CheckSubscriptionMiddleware())
    dp.callback_query.middleware(CheckSubscriptionMiddleware())
    dp.include_router(main_router)
    now = datetime.now(UTC) + timedelta(hours=5)

    await sender_function(
        bot,
        f"<b>✅ Bot successfully started</b>\n🕒 <i>{now.strftime('%d-%m-%Y %H:%M:%S')}</i> (UTC)",
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
