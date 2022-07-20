from aiogram import Bot, Dispatcher, executor, types
# import os
from aiogram.dispatcher.filters import Text
import json
bot = Bot(token="5492669742:AAENd4_UHTbJEpzVIsbiqAKLe_zB3sS_WMQ")
# bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Дать случайный фразеологизм", "Посмотреть сохранённые фразеологизмы"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Привет! Начнём?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Дать случайный фразеологизм"))
async def get_idiom(message: types.Message):
    await message.answer("Trying to beat the clock...")

    with open("data/idiom_info.json") as file:
        data = json.load(file)

    for idiom in data:

        await message.answer(idiom)


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
