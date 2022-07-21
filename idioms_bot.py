from aiogram import Bot, Dispatcher, executor, types
# import os
from aiogram.dispatcher.filters import Text
import json
import random


bot = Bot(token="5492669742:AAENd4_UHTbJEpzVIsbiqAKLe_zB3sS_WMQ")
# bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Give me an idiom", "Show me the idioms I've saved"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Hello! Let's get started?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Give me an idiom"))
async def get_idiom_name(message: types.Message):
    idiom_buttons = ["What does it mean?", "Give me some examples", "I've seen it. Give me another idiom"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*idiom_buttons)

    await message.answer("Just a moment. I'm trying to _beat the clock_...", parse_mode="Markdown")

    with open("data/idiom_info.json") as file:
        data = json.load(file)
        random_index = random.randint(0, len(list(data)) - 1)
        in_d = list(data.items())[random_index]
        name = in_d[1].get("idiom_name")

        await message.answer("The idiom is " + "*" + str(name) + "*", reply_markup=keyboard, parse_mode="Markdown")

        @dp.message_handler(Text(equals="What does it mean?"))
        async def get_idiom_meanings(second_message: types.Message):
            buttons = ["Thanks! Back to menu", "Give me some examples"] + \
                    ["I've seen it. Give me another idiom", "Add it to my list"]
            second_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            second_keyboard.add(*buttons)
            meanings = in_d[1].get("idiom_meaning")

            await second_message.answer("This idiom means: \n" + "_" +
                                        str(meanings).replace("END_LINE", "\n")
                                        + "_", reply_markup=keyboard, parse_mode="Markdown")

# def idiom_finder(d):
#     random_index = random.randint(0, len(list(d)) - 1)
#     in_d = list(d.items())[random_index]
#     print(in_d[1])
#     result = in_d[1].items()
#     return result


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
