from env_loading import ENV
from aiogram import Bot
from aiogram.types import PhotoSize, Document

from path_config import PREVIEW_IMG as PREVIEW_IMG_PATH
from path_config import PRESENTATIONS as PRESENTATIONS_PATH

bot = Bot(ENV.get("TOKEN"))

async def download_preview(filename:str, photo: PhotoSize):
    await bot.download(photo, PREVIEW_IMG_PATH.joinpath(filename))

async def download_document(filename:str, file: Document):
    await bot.download(file, PRESENTATIONS_PATH.joinpath(filename))