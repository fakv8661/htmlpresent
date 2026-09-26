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

def GetMainKeyboard(high_admin: bool=False):
    if not high_admin:
        return ADMIN_KB
    else:
        builder = InlineKeyboardBuilder.from_markup(ADMIN_KB)
        builder.row(InlineKeyboardButton(text="[*] Управление админами", callback_data="manage_admins"), 
            InlineKeyboardButton(text="[*] Управление презентациями", callback_data="manage_presentations"))
        return builder.as_markup()