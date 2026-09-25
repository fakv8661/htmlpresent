from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from env_loading import ENV

bot = Bot(ENV.get("TOKEN"))
dp = Dispatcher()

async def run_bot():
    print("Bot started")
    await dp.start_polling(bot, polling_timeout=30)