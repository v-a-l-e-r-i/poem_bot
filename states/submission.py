from aiogram.fsm.state import StatesGroup, State


class SubmissionStates(StatesGroup):
    waiting_for_poem = State()
    waiting_for_title = State()
    waiting_for_name = State()
    waiting_for_socials = State()
    waiting_for_permission = State()
