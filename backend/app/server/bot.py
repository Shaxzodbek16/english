import logging, sys, asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from app.api.routers.bot import main_router
from app.api.bot.main import get_bot
from app.core.settings import get_settings, Settings

settings: Settings = get_settings()

storage = RedisStorage.from_url(
    f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB + 1}")

dp = Dispatcher(storage=storage)


async def main() -> None:
    bot = await get_bot()
    dp.include_router(main_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
