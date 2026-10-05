from aiogram.fsm.state import StatesGroup, State

class PresentationAdd(StatesGroup):
    name = State()
    author = State()
    description = State()
    image = State()
    file = State()

class PresentationHide(StatesGroup):
    id = State()

class PresentationDelete(StatesGroup):
    id = State()

class AdminGet(StatesGroup):
    tg_id = State()
    login = State()

class AdminDel(StatesGroup):
    id = State()

class AdminNew(StatesGroup):
    login = State()
    telegram_id = State()