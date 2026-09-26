from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram import html

from Database.database import AdminPanel

class FAdmin(BaseFilter):
    def __init__(self, high_level: bool=False) -> None:
        self.high_level = high_level

    async def __call__(self, message: Message) -> bool:
        admincheck = await AdminPanel.AdminCheck(message.from_user.id, self.high_level)

        if not admincheck:
            await message.answer(f"[x] {html.bold(message.from_user.first_name)}, У вас нет прав на выполнение этой команды",
                                 parse_mode='HTML')

        return admincheck

class FMessageLen(BaseFilter):
    def __init__(self, max_len: int) -> None:
        self.max_len = max_len

    async def __call__(self, message: Message) -> bool:
        res = len(message.text) < self.max_len

        if not res:
            await message.answer(f"[!] Текст не может превышать {html.bold(self.max_len)} символов")

        return res