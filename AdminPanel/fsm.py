from aiogram.fsm.state import StatesGroup, State

class PresentationAdd(StatesGroup):
    name = State()
    author = State()
    description = State()
    image = State()
    file = State()