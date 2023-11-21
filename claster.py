from telebot.handler_backends import StatesGroup, State

class PollState(StatesGroup):
    name = State()
    age = State()
    command = State()
    rand = State()
    date = State()
    delt = State()

class HelpState(StatesGroup):
    wait_text = State()
