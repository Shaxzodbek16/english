from aiogram.types import BotCommand
from app.core.settings import get_settings, Settings
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode

settings: Settings = get_settings()


async def set_default_commands(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Start bot."),
            BotCommand(command="lang", description="Change language."),
            BotCommand(command="quiz", description=f"Get quiz for today."),
            BotCommand(command="help", description="Get help."),
        ]
    )


dp = Dispatcher()


async def get_bot() -> Bot:
    if settings.DEBUG:
        print("Running in DEBUG mode. Bot token is:", settings.BOT_TOKEN)
        bot = Bot(
            token=settings.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
        )
    else:
        local_server = TelegramAPIServer.from_base("http://localhost:8081")
        bot = Bot(
            token=settings.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
            server=local_server,
        )
    await set_default_commands(bot)
    return bot
