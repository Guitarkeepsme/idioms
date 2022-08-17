from aiogram import types
from aiogram.dispatcher.filters import Text

from data import bot_messages
from data.config import cursor, connection, Form
from handlers.random_idiom_commands import first_step
from loader import dp


@dp.message_handler(commands="start", state='*')
async def start(message: types.Message):
    button = ["Ok. Let's begin!"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*button)
    cursor.execute('INSERT OR IGNORE INTO Users (ID) VALUES (:ID)', (message.from_user.id,))
    connection.commit()
    await Form.idiom.set()
    await message.answer("Hello, " + "*" + message.from_user.first_name +
                         "*! 👋 " + bot_messages.start_message, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text not in bot_messages.commands, state=Form.idiom)
async def invalid_message(message: types.Message):
    return await message.reply("I don't know what you mean. Please check current commands.")


@dp.message_handler(Text(equals="Back to menu"), state='*')
async def go_back(message: types.Message):
    await Form.idiom.set()
    await first_step(message)
