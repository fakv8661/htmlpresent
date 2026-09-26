from aiogram import Dispatcher, F, html
from aiogram.types import Message, CallbackQuery, PhotoSize
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from AdminPanel.bot_config import bot
from Database import models
from Database.database import AdminPanel, PresentationDatabase
from AdminPanel import filter as tgfil
from AdminPanel import keyboard
from AdminPanel import fsm
from AdminPanel import fsm_router
import utils

dp = Dispatcher()

@dp.message(CommandStart())
async def startcmd(message: Message):
    admin_id = await AdminPanel.GetAdminIDByTg(message.from_user.id)
    if await AdminPanel.AdminCheck(message.from_user.id):
        await message.answer(f"[~] {html.bold(message.from_user.first_name)}, Админ-панель открыта", 
                             parse_mode='HTML', reply_markup=keyboard.GetMainKeyboard(await AdminPanel.isHighAdmin(admin_id)))
    else: 
        await message.answer(f"[x] {html.bold(message.from_user.first_name)}, у вас нет доступа к этому боту!\n[?] Для получения доступа обратитесь к администрации.\n[*] Ваш UID: {html.italic(str(message.from_user.id))}",
                             parse_mode='HTML')

@dp.callback_query(F.data == "presentation_add", tgfil.FAdmin(False))
async def presentation_add(callback: CallbackQuery, state: FSMContext):
    message = callback.message
    admin_id = await AdminPanel.GetAdminIDByTg(callback.from_user.id)

    if await AdminPanel.isHighAdmin(admin_id) or not await AdminPanel.PresentationLimitCheck(admin_id):
        await message.answer("[+] Отправьте название презентации")
        await state.set_state(fsm.PresentationAdd.name)
    else:
        await message.answer("[!] Вы достигли лимита презентаций")

@dp.callback_query(F.data == "presentation_local", tgfil.FAdmin(False))
async def presentation_local(callback: CallbackQuery):
    presentation_msg = utils.get_localpresentations_msg(callback.from_user.first_name,
                                                        await PresentationDatabase.GetPresentationsByOwner(
                                                            await AdminPanel.GetAdminIDByTg(callback.from_user.id)
                                                        ))
    await callback.message.answer(presentation_msg, parse_mode='HTML')

@dp.callback_query(F.data == "presentation_manage_hideshow", tgfil.FAdmin(False))
async def presentation_manage_hideshow(callback: CallbackQuery):
    ...

async def run_bot():
    print("[Telegram] Bot started")
    dp.include_router(fsm_router.router)
    await dp.start_polling(bot, polling_timeout=30)