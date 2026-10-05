from copy import deepcopy
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

ADMIN_KB = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="[+] Добавить презентацию в БД", callback_data="presentation_add")],
    [InlineKeyboardButton(text="[=] Мои презентации", callback_data="presentation_local")]
])

IMGPREVIEW_SELECTOR = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="[X] Оставить пустым", callback_data="presentation_add_image_null")],
    [InlineKeyboardButton(text="[-] Отмена", callback_data="fsm_cancel")]
])

PRESENTATION_LOCAL_MANAGE = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="[-] Скрыть/показать презентацию", callback_data="presentation_manage_hideshow")],
    [InlineKeyboardButton(text="[=] Изменить параметр", callback_data="presentation_manage_change")],
    [InlineKeyboardButton(text="[-] Удалить презентацию", callback_data="presentation_manage_delete")]
])

ADMIN_MANAGE = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="[=] Все админы", callback_data="manage_admins_all")],
    [InlineKeyboardButton(text="[+] Добавить админа", callback_data="manage_admins_add")],
    [InlineKeyboardButton(text="[-] Удалить админа", callback_data="manage_admins_del")],
    [InlineKeyboardButton(text="[?] Получить ID (TG ID)", callback_data="manage_admins_get_tg"),
     InlineKeyboardButton(text="[?] Получить ID (LOGIN)", callback_data="manage_admins_get_login")]
])

ADMIN_MANAGE_LOGIN = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="[X] Оставить пустым", callback_data="manage_admins_login_null")],
    [InlineKeyboardButton(text="[-] Выйти", callback_data="fsm_cancel")]
])

def GetMainKeyboard(high_admin: bool=False) -> InlineKeyboardMarkup:
    if not high_admin:
        return deepcopy(ADMIN_KB)
    else:
        builder = InlineKeyboardBuilder.from_markup(deepcopy(ADMIN_KB))
        builder.row(InlineKeyboardButton(text="[*] Управление админами", callback_data="manage_admins"), 
            InlineKeyboardButton(text="[*] Управление презентациями", callback_data="manage_presentations"))
        return builder.as_markup()

def GetShowHidePresentationKb(hidden: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if hidden:
        builder.add(InlineKeyboardButton(text="[+] Показать", callback_data="presentation_manage_show"))
    else:
        builder.add(InlineKeyboardButton(text="[-] Скрыть", callback_data="presentation_manage_hide"))

    builder.row(InlineKeyboardButton(text="[x] Отмена", callback_data="fsm_cancel"))
    return builder.as_markup()