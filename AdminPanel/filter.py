from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import html

from Database.database import AdminPanel, PresentationDatabase

class FAdmin(BaseFilter):
    def __init__(self, high_level: bool=False) -> None:
        self.high_level = high_level

    async def __call__(self, message: Message) -> bool:
        admincheck = await AdminPanel.AdminCheck(message.from_user.id, self.high_level)

        if not admincheck:
            await message.answer(f"🚫 {html.bold(message.from_user.first_name)}, У вас нет прав на выполнение этой команды",
                                 parse_mode='HTML')

        return admincheck

class FMessageLen(BaseFilter):
    def __init__(self, max_len: int) -> None:
        self.max_len = max_len

    async def __call__(self, message: Message) -> bool:
        res = len(message.text) < self.max_len

        if not res:
            await message.answer(f"⚠️ Текст не может превышать {html.bold(self.max_len)} символов")

        return res

class FPOwnCheck(BaseFilter):
    def __init__ (self, state_key: str='id'):
        self.state_key = state_key
    """Необходимо чтобы message.text являлся ID презентации или он был в state, иначе будет не то!!!"""
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        if state.get_state() is None:
            await message.answer("⚠️ FSM error")
            return False
        
        admin_id = await AdminPanel.GetAdminIDByTg(message.from_user.id)
        presentation_id = None
        try:
            if not message.text.isnumeric():
                await message.answer("⚠️ Это не ID презентации")
                await state.clear()
                return False
            presentation_id = int(message.text)
        except AttributeError:
            presentation_id = await state.get_value(self.state_key)

        if presentation_id is None:
            await message.answer("⚠️ ID презентации не найден")
            return False

        
        presentation = await PresentationDatabase.GetPresentationByID(presentation_id, True)
        high_admin = await AdminPanel.isHighAdmin(admin_id)
    
        if presentation.owner_id != admin_id and not high_admin:
            await message.answer("⚠️ Это не ваша презентация")
            await state.clear()
            return False
        
        return True

class FNumeric(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        filt = message.text.isnumeric()

        if not filt:
            await message.answer("⚠️ Это не число")

        return filt