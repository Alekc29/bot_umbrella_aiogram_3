from aiogram.fsm.state import State, StatesGroup


class FSMTown(StatesGroup):
    town = State()
    reminder_time = State()


class FSMWish(StatesGroup):
    wish = State()


class FSMPost(StatesGroup):
    post = State()
