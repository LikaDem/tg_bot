import os

import telebot
import random
import claster

from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()

bot = telebot.TeleBot("6876022372:AAEiZlNGN3yJcin4azM058RQwcHpDbtNEtk",
                      state_storage=state_storage, parse_mode='Markdown')

RANDOM_TASKS = ["Покормить кошку", "Помыть машину", "Заботать физику", "Заботать прогу"]

HELP = """
/hi - бот познакомится с Вами.
/help - вывести список доступных команд.
/add - добавить задачу в виде: <дата> <задача>.
/show - вывести все задачи.
/random - добавить случайную задачу на введенную дату.
/delete - удалить задачу
"""

tasks = {}


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        f'Привет, {message.from_user.first_name}! Я бот-планер.🤖' + '\n' +
        'Помогу спланировать твой день!' + '\n' + HELP)


@bot.message_handler(func=lambda message: '/hi' == message.text)
def first(message):
    bot.send_message(message.chat.id, '_Ваше имя_?')
    bot.set_state(message.from_user.id, claster.PollState.name, message.chat.id)

@bot.message_handler(state=claster.PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Супер! _Ваш возраст?_')
    bot.set_state(message.from_user.id, claster.PollState.age, message.chat.id)

@bot.message_handler(state=claster.PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Приятно познакомиться!')
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: '/help' == message.text)
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(func=lambda message: '/add' == message.text)
def add(message):
    bot.send_message(message.chat.id, ' Введите: <дата> <задача>')
    bot.set_state(message.from_user.id, claster.PollState.command, message.chat.id)

@bot.message_handler(state=claster.PollState.command)
def add_task(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = message.text
    command = message.text.split(maxsplit=1)
    date = command[0]
    task = command[1]
    with open(f'{date}.txt', 'a') as f:
        f.write(task + '\n')
    text = 'Задача ' + task + ' добавлена на ' + date
    bot.send_message(message.chat.id, text)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: '/random' == message.text)
def add_random_task(message):
    bot.send_message(message.chat.id, ' Введите дату')
    bot.set_state(message.from_user.id, claster.PollState.rand, message.chat.id)

@bot.message_handler(state=claster.PollState.rand)
def random_name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['rand'] = message.text
    date = message.text
    task = random.choice(RANDOM_TASKS)
    with open(f'{date}.txt', 'a') as f:
        f.write(task + '\n')
    text = 'Задача ' + task + ' добавлена на ' + date
    bot.send_message(message.chat.id, text)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: '/show' == message.text)
def show(message):
    bot.send_message(message.chat.id, 'Введите дату')
    bot.set_state(message.from_user.id, claster.PollState.date, message.chat.id)

@bot.message_handler(state=claster.PollState.date)
def show_task(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['date'] = message.text
    da = message.text
    text = ''
    with open(f'{da}.txt', 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            bot.send_message(message.chat.id, line)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: '/delete' == message.text)
def add_random_task(message):
    bot.send_message(message.chat.id, ' Введите: <дата> <задача>')
    bot.set_state(message.from_user.id, claster.PollState.delt, message.chat.id)

@bot.message_handler(state=claster.PollState.delt)
def random_name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['delt'] = message.text
    command = message.text.split(maxsplit=1)
    date = command[0]
    task = command[1]
    with open(f'{date}.txt', "r") as f:
        lines = f.readlines()
    with open(f'{date}.txt', "w") as f:
        for line in lines:
            if line.strip("\n") != task:
                f.write(line)

    text = 'Хорошая работа!'
    bot.send_message(message.chat.id, text)
    bot.delete_state(message.from_user.id, message.chat.id)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.polling(none_stop=True)
