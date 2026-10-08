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
import logs

dp = Dispatcher()
LOGI = logs.getLogger(__file__)

@dp.message(CommandStart())
async def startcmd(message: Message):
    admin_id = await AdminPanel.GetAdminIDByTg(message.from_user.id)
    if await AdminPanel.AdminCheck(message.from_user.id):
        await message.answer(f"🛠️ {html.bold(message.from_user.first_name)}, Админ-панель открыта", 
                             parse_mode='HTML', reply_markup=keyboard.GetMainKeyboard(await AdminPanel.isHighAdmin(admin_id)))
    else: 
        await message.answer(f"🚫 {html.bold(message.from_user.first_name)}, у вас нет доступа к этому боту!\n🆔 Для получения учетной записи обратитесь к администрации или авторизуйтесь через логин, пароль.\n💡 Ваш UID: {html.italic(str(message.from_user.id))}",
                             parse_mode='HTML',
                             reply_markup=keyboard.AUTH_KEYBOARD)
        LOGI.info("User (%s) tried to get access to bot", message.from_user.id)

@dp.callback_query(F.data == "presentation_add", tgfil.FAdmin(False))
async def presentation_add(callback: CallbackQuery, state: FSMContext):
    message = callback.message
    admin_id = await AdminPanel.GetAdminIDByTg(callback.from_user.id)

    if await AdminPanel.isHighAdmin(admin_id) or not await AdminPanel.PresentationLimitCheck(admin_id):
        await message.answer("✅ Отправьте название презентации")
        await state.set_state(fsm.PresentationAdd.name)
    else:
        await message.answer("⚠️ Вы достигли лимита презентаций")

@dp.callback_query(F.data == "presentation_local", tgfil.FAdmin(False))
async def presentation_local(callback: CallbackQuery):
    presentation_msg = utils.get_localpresentations_msg(callback.from_user.first_name,
                                                        await PresentationDatabase.GetPresentationsByOwner(
                                                            await AdminPanel.GetAdminIDByTg(callback.from_user.id)
                                                        ))
    await callback.message.answer(presentation_msg, parse_mode='HTML', reply_markup=keyboard.PRESENTATION_LOCAL_MANAGE)

@dp.callback_query(F.data == "presentation_manage_hideshow", tgfil.FAdmin(False))
async def presentation_manage_hideshow(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✅ Отправьте ID презентацию, которую хотите показать/скрыть")
    await state.set_state(fsm.PresentationHide.id)

@dp.callback_query(F.data == "presentation_manage_delete", tgfil.FAdmin(False))
async def presentation_manage_delete(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✅ Отправьте ID презентации, которую хотите удалить")
    await state.set_state(fsm.PresentationDelete.id)  

@dp.callback_query(F.data == "manage_presentations", tgfil.FAdmin(True))
async def manage_presentationsf(callback: CallbackQuery):
    presentations = await PresentationDatabase.GetAllPresentations(True)

    await callback.message.answer(utils.get_localpresentations_msg(callback.from_user.first_name, presentations),
                                  parse_mode='HTML',
                                  reply_markup=keyboard.PRESENTATION_LOCAL_MANAGE)

@dp.callback_query(F.data == "manage_admins", tgfil.FAdmin(True))
async def manage_admins(callback: CallbackQuery):
    await callback.message.answer("💡 Выберите подпункт", reply_markup=keyboard.ADMIN_MANAGE)

@dp.callback_query(F.data == "manage_admins_all", tgfil.FAdmin(True))
async def manage_admins_all(callback: CallbackQuery):
    admins = await AdminPanel.GetAllAdmins()
    msg = "📋 Формат вылачи (ID, TG ID, LOGIN)\nВсе админы:\n"

    for admin in admins:
        msg += str(admin)
    
    await callback.message.answer(msg)

@dp.callback_query(F.data == "manage_admins_get_tg", tgfil.FAdmin(True))
async def manage_admins_get_tg(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🆔 Отправьте Telegram ID пользователя")
    await state.set_state(fsm.AdminGet.tg_id)

@dp.callback_query(F.data == "manage_admins_get_login", tgfil.FAdmin(True))
async def manage_admins_get_tg(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🆔 Отправьте логин пользователя")
    await state.set_state(fsm.AdminGet.login)

@dp.callback_query(F.data == "manage_admins_del", tgfil.FAdmin(True))
async def manage_admins_del(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✅ Отправьте ID (не telegram id) пользователя")
    await state.set_state(fsm.AdminDel.id)

@dp.callback_query(F.data == "manage_admins_add", tgfil.FAdmin())
async def manage_admins_add(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✅ Придумайте логин, (Пример: ФамилияИмя)")
    await state.set_state(fsm.AdminNew.login)

@dp.callback_query(F.data == "admin_auth")
async def admin_auth(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🖊️ Отправьте ваш логин")
    await state.set_state(fsm.AdminAuth.login)


async def run_bot():
    dp.include_router(fsm_router.router)
    LOGI.info("Telegram bot starting")
    await dp.start_polling(bot, polling_timeout=30)