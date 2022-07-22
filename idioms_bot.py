from aiogram import Bot, Dispatcher, executor, types
# import os
from aiogram.dispatcher.filters import Text
import json
import random

bot = Bot(token="5492669742:AAENd4_UHTbJEpzVIsbiqAKLe_zB3sS_WMQ", parse_mode="Markdown")
# bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)

with open("data/idiom_info.json") as file:
    data = json.load(file)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_button = ["Ok. Let's begin!"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)
    await message.answer("Hello, " + "*" + message.from_user.first_name +
                         "*! 👋" + "I'll help you to learn new idioms. " +
                         "Here are the list of my functions: \n\n - Giving random idiom with " +
                         "meanings and examples in sentences;" +
                         "\n\n - Collecting the idioms you want to save; (*in development*)" +
                         "\n\n - Searching for an idiom in my library; (*in development*)" +
                         "\n\n - Finding definitions and translations of the words; " +
                         "(*in development*)" + "\n\nThe functions which are being developed " +
                         "will appear during the next few weeks. _Stay tuned!_ 👨‍💻" +
                         "\n\n\nPlease share your thoughts and ideas about my work " +
                         "with my creator @Dontwait", reply_markup=keyboard)


@dp.message_handler(Text(equals="Ok. Let's begin!"))
async def first_step(message: types.Message):
    start_buttons = ["Give me an idiom", "Show me the idioms I've saved", "I want to search for an idiom"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*start_buttons)
    await message.answer("Are you ready to _dive into_ idioms?", reply_markup=keyboard)


# async def get_idiom_name(message: types.Message):
#     if message.text.lower() == "give me an idiom":
#         try:
#             idiom_buttons = ["No. What does it mean?", "I've seen it. Give me another one", "Back to menu"]
#             keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#             keyboard.add(*idiom_buttons)
#             await message.answer("Just a moment. I'm trying to _beat the clock_...")
#
#             random_index = random.randint(0, len(list(data)) - 1)
#             global in_d
#             in_d = list(data.items())[random_index]
#             name = in_d[1].get("idiom_name")
#             await message.answer("The idiom is " + "*" + str(name) + "*. "
#                                  + "Have you already seen this one?", reply_markup=keyboard)
#         except Exception as ex:
#             print(ex)
#             await message.answer("Damn...Something was wrong...")
#
#     else:
#         await message.answer("I don't know what you mean. Look at the commands")


@dp.message_handler(Text(equals="Give me an idiom"))
async def get_idiom_name(message: types.Message):
    idiom_buttons = ["No. What does it mean?", "I've seen it. Give me another one", "Back to menu"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*idiom_buttons)
    await message.answer("Just a moment. I'm trying to _beat the clock_...")

    random_index = random.randint(0, len(list(data)) - 1)
    global in_d
    in_d = list(data.items())[random_index]
    name = in_d[1].get("idiom_name")
    await message.answer("The idiom is " + "*" + str(name) + "*. "
                     + "Have you already seen this one?", reply_markup=keyboard)


@dp.message_handler(Text(equals="No. What does it mean?"))
async def get_idiom_meanings(second_message: types.Message):
    buttons = ["Show me some examples", "I've seen it. Give me another one", "Back to menu"]
    second_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    second_keyboard.add(*buttons)
    meanings = in_d[1].get("idiom_meaning")

    await second_message.answer("This idiom means: \n \n - " + "_" +
                                str(meanings).replace("END_LINE", "\n \n - ")[0:-3]
                                + "_", reply_markup=second_keyboard)


@dp.message_handler(Text(equals="Show me some examples"))
async def get_idiom_examples(third_message: types.Message):
    buttons = ["I've seen it. Give me another one", "Add this idiom to my collection", "Back to menu"]
    second_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    examples = in_d[1].get("idiom_examples")
    second_keyboard.add(*buttons)
    # попытаться как-то выделить жирным шрифтом идиомы внутри примеров
    await third_message.answer("Here are some examples: \n \n - " + "_" +
                               str(examples).replace("END_LINE", "\n \n - ")[0:-3]
                               + "_", reply_markup=second_keyboard)


@dp.message_handler(Text(equals="Back to menu"))
async def go_back(start_message: types.Message):
    await first_step(start_message)


@dp.message_handler(Text(equals="I've seen it. Give me another one"))
async def go_another(another_message: types.Message):
    await get_idiom_name(another_message)


@dp.message_handler(Text(equals="Show me the idioms I've saved"))
async def get_idioms_list(message: types.Message):
    await message.answer("_Hold your horses_. This function is being developed.")


@dp.message_handler(Text(equals="I want to search for an idiom"))
async def get_idioms_list(message: types.Message):
    await message.answer("Don't _jump the gun_! This function is being developed.")


@dp.message_handler(Text(equals="Add this idiom to my collection"))
async def get_idioms_list(message: types.Message):
    await message.answer("The secret of this function _has been lost in the mists of time_... " +
                         "But I am recovering it.")


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
