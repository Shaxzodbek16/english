import asyncio, logging,sys
from aiogram import Bot, Dispatcher

from app.bot.routers.users import router as user_router
from app.core.settings import get_settings


async def main() -> None:
    settings = get_settings()
    bot = Bot(settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(user_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
