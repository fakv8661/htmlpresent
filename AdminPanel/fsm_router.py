import time
import os
    
from aiogram import Router, F, html
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import invert_f
from pydantic import ValidationError

from Database.database import AdminPanel, PresentationDatabase
from AdminPanel import filter as tgfil
from AdminPanel import fsm
from AdminPanel import keyboard
from AdminPanel.bot_config import download_preview, download_document
import path_config
import utils
from AdminPanel import validation as valid
import keygen
import logs

router = Router(name="fsm_router")
LOGI = logs.getLogger(__file__)

#------------------FSM OTHER---------------------
@router.callback_query(F.data == "fsm_cancel")
async def fsm_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("❌ Отменено")
    await state.clear()
# ------------------------------------------------

#----------------- PRESENTATION ADD---------------------
@router.message(fsm.PresentationAdd.name)
async def presentationadd_name(message: Message, state: FSMContext):
    await message.answer("✅ Отправьте авторов презентации (Формата: ФИО, ФИО, ФИО)")
    await state.update_data(name=message.text)
    await state.set_state(fsm.PresentationAdd.author)

@router.message(fsm.PresentationAdd.author)
async def presentationadd_author(message: Message, state: FSMContext):
    await message.answer("✅ Отправьте описание, не более 500 символов")
    await state.update_data(author=message.text)
    await state.set_state(fsm.PresentationAdd.description)

@router.message(fsm.PresentationAdd.description)
async def presentationadd_description(message: Message, state: FSMContext):
    await message.answer("✅ Отправьте превью презентации (Отправлять только в виде изображения!!!)",
                         reply_markup=keyboard.IMGPREVIEW_SELECTOR)
    await state.update_data(description=message.text)
    await state.set_state(fsm.PresentationAdd.image)

@router.message(invert_f(F.photo), fsm.PresentationAdd.image)
async def presentationadd_image_notimg(message: Message, state: FSMContext):
    await message.answer("⚠️ Фото не обнаружено")

@router.message(F.photo, fsm.PresentationAdd.image)
async def presentationadd_image(message: Message, state: FSMContext):
    photo = message.photo[-1]
    timenow = time.time()
    filename = f"{message.from_user.id}_{round(timenow)}.jpg"
    await download_preview(filename ,photo)
    await message.answer("✅ Отправьте фаил презентации")
    await state.update_data(image=filename)
    await state.set_state(fsm.PresentationAdd.file)

@router.callback_query(F.data == "presentation_add_image_null")
async def presentationadd_null(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✅ Отправьте фаил презентации")
    await state.update_data(image=None)
    await state.set_state(fsm.PresentationAdd.file)

@router.message(F.document, fsm.PresentationAdd.file)
async def presentationadd_document(message: Message, state: FSMContext):
    document = message.document

    filetype = utils.get_filetype(document.file_name)
    if filetype is None:
        await message.answer("⚠️ Не удалось определить тип файла")
        return
    timenow = time.time()
    filename = f"{message.from_user.id}_{round(timenow)}.{filetype}"
    await state.update_data(file=filename)
    await download_document(filename, document)
    await message.answer("⏳ Проверка верной загрузки файлов...")

    img_preview = await state.get_value("image")

    if not os.path.exists(path_config.PRESENTATIONS.joinpath(filename)):
        if img_preview is not None and not os.path.exists(path_config.PREVIEW_IMG.joinpath(img_preview)):
                await message.answer("⚠️ Файлы не были верно загружены. Попробуйте снова!")
                await state.clear()
                return
    data = await state.get_data()
    try:
        padd_schema = valid.PresentationAddSchema.model_validate(data)
    except ValidationError:
        await message.answer("⚠️ Валидация отправленных данных не прошла")
        await state.clear()
        return

    admin_id = await AdminPanel.GetAdminIDByTg(message.from_user.id)
    if admin_id is None:
        await message.answer("⚠️ Admin ID утерян. Попробуйте снова!")
        await state.clear()
        return
    
    await PresentationDatabase.CreatePresentation(
        padd_schema.name,
        padd_schema.author,
        padd_schema.description,
        str(padd_schema.file),
        padd_schema.image if padd_schema.image is None else str(padd_schema.image),
        admin_id
    )

    await message.answer("✅ Запрос на создание презентации отправлен")
    LOGI.info("Presentation %s is created; File: %s; Image: %s; Owner: %s", 
              padd_schema.name, padd_schema.file, padd_schema.image, admin_id)
    await state.clear()

#------------------------------------------

#--------------PRESENTATION HIDE-------------
@router.message(fsm.PresentationHide.id, tgfil.FPOwnCheck())
async def presentationhide_id(message: Message, state: FSMContext):
    presentation_id = int(message.text)
    presentation = await PresentationDatabase.GetPresentationByID(presentation_id, True)

    await state.update_data(id=presentation_id)
    await message.answer(f"ℹ️ Выберите действие\nПрезентация: {html.bold("Скрыта" if presentation.hidden else "Доступна")}",
                         parse_mode='HTML',
                         reply_markup=keyboard.GetShowHidePresentationKb(presentation.hidden))


@router.callback_query(F.data.in_({'presentation_manage_show', 'presentation_manage_hide'}), 
                       fsm.PresentationHide.id, tgfil.FPOwnCheck())
async def presentationmanage_hide(callback: CallbackQuery, state: FSMContext):
    message = callback.message

    presentation_id = await state.get_value("id")
    
    if presentation_id is None:
        await state.clear()
        await message.answer("⚠️ ID не найден")
        return

    presentation = await PresentationDatabase.GetPresentationByID(presentation_id, True)

    if presentation is None:
        await state.clear()
        await message.answer("⚠️ Презентация не найдена")
        return

    await message.answer(f"ℹ️ Выберите действие\nПрезентация: {html.bold("Скрыта" if not presentation.hidden else "Доступна")}",
                            parse_mode='HTML',
                            reply_markup=keyboard.GetShowHidePresentationKb(not presentation.hidden))


    await PresentationDatabase.HidePresentation(presentation_id, not presentation.hidden)

#----------------------------------------

#--------------------------------- PRESENTATION DELETE 
@router.message(fsm.PresentationDelete.id,
                tgfil.FPOwnCheck())
async def presentation_manage_delete_id(message: Message, state: FSMContext):
    presentation_id = int(message.text)
    presentation = await PresentationDatabase.GetPresentationByID(presentation_id, True)

    if presentation is None:
        await state.clear()
        await message.answer("⚠️ Презентация не найдена")

    await PresentationDatabase.DeletePresentation(presentation_id)
    LOGI.info("Presentation %s deleted by admin (%s)", presentation.name, message.from_user.id)
    await message.answer("❌ Презентация удалена")
# ------------------------------------------------

#--------------------------------ADMIN GET

@router.message(fsm.AdminGet.tg_id, tgfil.FNumeric())
async def manage_admins_get_tg_fsm(message: Message, state: FSMContext):

    admin = await AdminPanel.GetAdminIDByTg(int(message.text))

    if admin is not None:
        await message.answer(f"🆔 Получен ID: {html.italic(admin)}", parse_mode='HTML')
    else:
        await message.answer("⚠️ Пользователь не найден")

    await state.clear()

@router.message(fsm.AdminGet.login)
async def manage_admins_get_tg_fsm(message: Message, state: FSMContext):
    admin = await AdminPanel.GetAdminIDByLogin(message.text)

    if admin is not None:
        await message.answer(f"🆔 Получен ID: {html.italic(admin)}", parse_mode='HTML')
    else:
        await message.answer("⚠️ Пользователь не найден")

    await state.clear()

#------------------------------------

#------------------------ADMIN DEL
@router.message(fsm.AdminDel.id, tgfil.FNumeric())
async def manage_admins_del_fsm(message: Message, state: FSMContext):
    if AdminPanel.isHighAdmin(int(message.text)):
        await message.answer("⚠️ Снять выс. админа нельзя")
        await state.clear()
        return
    await AdminPanel.DeleteAdmin(int(message.text))
    LOGI.info("Admin %s removed from database by admin (%s)", message.text, message.from_user.id)
    await message.answer("❌ Запрос на удаление отправлен")
    await state.clear()
#---------------------------------

#----------------------ADMIN NEW
@router.message(fsm.AdminNew.login)
async def manage_admins_add_pre_login(message: Message, state: FSMContext):
    login = message.text

    if not login:
        await message.answer("⚠️ Сообщение пустое")
        return

    login = keygen.generate_login(login)
    unique_login = keygen.unique_login(login)
    logincheck = await AdminPanel.GetAdminIDByLogin(unique_login)

    while logincheck:
        unique_login = keygen.unique_login(login)
        logincheck = await AdminPanel.GetAdminIDByLogin(unique_login)

    await message.answer(f"🔑 Логин сгенерирован\n{html.bold(unique_login)}", parse_mode='HTML')
    await state.update_data(login=unique_login)
    await message.answer("✅ Отправьте Telegram ID (если есть)", reply_markup=keyboard.ADMIN_MANAGE_LOGIN)
    await state.set_state(fsm.AdminNew.telegram_id)

@router.callback_query(F.data == "manage_admins_login_null", fsm.AdminNew.telegram_id)
async def manage_admins_add_tgid_null(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✅ Оставлено пустым")

    login = await state.get_value("login")

    if not login:
        await callback.message.answer("⚠️ Логин утерян")
        await state.clear()
        return

    password = keygen.generate_password()
    password_hashed = utils.hash_password(password)

    await AdminPanel.CreateAdmin(login, password_hashed)
    await callback.message.answer(f"🔑 Пользователь создан!\nЛогин: {html.bold(login)}\nПароль: {html.spoiler(password)}",
                                  parse_mode='HTML')
    LOGI.info("Created new user with login: %s", login)
    await state.clear()

@router.message(fsm.AdminNew.telegram_id, tgfil.FNumeric())
async def managae_admins_add_tgid(message: Message, state: FSMContext):
    tg_id = int(message.text)

    login = await state.get_value("login")
    
    if not login:
        await message.answer("⚠️ Логин утерян")
        await state.clear()
        return

    password = keygen.generate_password()
    password_hashed = utils.hash_password(password)

    await AdminPanel.CreateAdmin(login, password_hashed, telegram_id=tg_id)
    await message.answer(f"🔑 Пользователь создан!\nЛогин: {html.bold(login)}\nПароль: {html.spoiler(password)}",
                         parse_mode='HTML')
    LOGI.info("Created new user with login: %s", login)
    await state.clear()

#-----------------------------

#---------------------- ADMIN AUTH
@router.message(fsm.AdminAuth.login)
async def admin_auth_login(message: Message, state: FSMContext):
    admin = await AdminPanel.GetAdminIDByLogin(message.text)

    if not admin:
        await message.answer("❌ Учетной записи под данным логином не существует")
        await state.clear()
        return

    await message.answer("🔑 Отправьте ваш пароль")
    await state.update_data(login=message.text)
    await state.set_state(fsm.AdminAuth.password)

@router.message(fsm.AdminAuth.password)
async def admin_auth_password(message: Message, state: FSMContext):
    admin = await AdminPanel.GetAdminIDByLogin(await state.get_value("login"))
    pwd_hash = await AdminPanel.GetHashPassword(admin)

    if not utils.verify_password(message.text, pwd_hash):
        await message.answer("❌ Пароль не подходит")
        await state.clear()
        return

    await message.answer("👤 Вы авторизованы. Телеграм связан с вашей учетной записью")
    LOGI.info("Linked telegram (%s) with user (%s)", message.from_user.id, admin)
    await state.clear()
    await AdminPanel.LinkTelegram(admin, message.from_user.id)
#--------------------------------