import time
import os
    
from aiogram import Router, F, html
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import invert_f

from Database.database import AdminPanel, PresentationDatabase
from AdminPanel import filter as tgfil
from AdminPanel import fsm
from AdminPanel import keyboard
from AdminPanel.bot_config import download_preview, download_document
import path_config

router = Router(name="fsm_router")

#------------------FSM OTHER---------------------
@router.callback_query(F.data == "fsm_cancel")
async def fsm_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("[-] Отменено")
    await state.clear()
# ------------------------------------------------

#----------------- PRESENTATION ADD---------------------
@router.message(fsm.PresentationAdd.name, tgfil.FMessageLen(256))
async def presentationadd_name(message: Message, state: FSMContext):
    await message.answer("[+] Отправьте авторов презентации (Формата: ФИО, ФИО, ФИО)")
    await state.update_data(name=message.text)
    await state.set_state(fsm.PresentationAdd.author)

@router.message(fsm.PresentationAdd.author, tgfil.FMessageLen(256))
async def presentationadd_author(message: Message, state: FSMContext):
    await message.answer("[+] Отправьте описание, не более 500 символов")
    await state.update_data(author=message.text)
    await state.set_state(fsm.PresentationAdd.description)

@router.message(fsm.PresentationAdd.description, tgfil.FMessageLen(500))
async def presentationadd_description(message: Message, state: FSMContext):
    await message.answer("[+] Отправьте превью презентации (Отправлять только в виде изображения!!!)",
                         reply_markup=keyboard.IMGPREVIEW_SELECTOR)
    await state.update_data(description=message.text)
    await state.set_state(fsm.PresentationAdd.image)

@router.message(invert_f(F.photo), fsm.PresentationAdd.image)
async def presentationadd_image_notimg(message: Message, state: FSMContext):
    await message.answer("[!] Фото не обнаружено")

@router.message(F.photo, fsm.PresentationAdd.image)
async def presentationadd_image(message: Message, state: FSMContext):
    photo = message.photo[-1]
    timenow = time.time()
    filename = f"{message.from_user.id}_{round(timenow)}.jpg"
    await download_preview(filename ,photo)
    await message.answer("[+] Отправьте фаил презентации")
    await state.update_data(image=filename)
    await state.set_state(fsm.PresentationAdd.file)

@router.callback_query(F.data == "presentation_add_image_null")
async def presentationadd_null(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("[+] Отправьте фаил презентации")
    await state.update_data(image=None)
    await state.set_state(fsm.PresentationAdd.file)

@router.message(F.document, fsm.PresentationAdd.file)
async def presentationadd_document(message: Message, state: FSMContext):
    document = message.document

    filetype = document.file_name.rsplit(".", 1)[-1].lower() if "." in document.file_name else None
    if filetype is None:
        await message.answer("[!] Не удалось определить тип файла")
        return
    timenow = time.time()
    filename = f"{message.from_user.id}_{round(timenow)}.{filetype}"
    await download_document(filename, document)
    await message.answer("[%] Проверка верной загрузки файлов...")

    img_preview = await state.get_value("image")

    if not os.path.exists(path_config.PRESENTATIONS.joinpath(filename)):
        if img_preview is not None and not os.path.exists(path_config.PREVIEW_IMG.joinpath(img_preview)):
                await message.answer("[!] Файлы не были верно загружены. Попробуйте снова!")
                await state.clear()
                return

    admin_id = await AdminPanel.GetAdminIDByTg(message.from_user.id)

    if admin_id is None:
        await message.answer("[!] Admin ID утерян. Попробуйте снова!")
        await state.clear()
        return
    
    await PresentationDatabase.CreatePresentation(
        await state.get_value("name"),
        await state.get_value("author"),
        await state.get_value("description"),
        filename,
        img_preview,
        admin_id
    )

    await message.answer("[+] Запрос на создание презентации отправлен")
    await state.clear()