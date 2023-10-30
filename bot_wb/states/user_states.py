from aiogram.dispatcher.filters.state import StatesGroup, State
class main(StatesGroup):
    default = State()
    new = State()