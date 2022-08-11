from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.dispatcher import FSMContext
import json
import random
import config
# import asyncio
from data import bot_messages
bot = Bot(token=config.TOKEN, parse_mode="Markdown")
dp = Dispatcher(bot)

with open("data/idiom_info.json", encoding='utf-8', newline='') as file:
    data = json.load(file)


# # States
# class Form(StatesGroup):
#     idiom_example = State()
#     sentences_example = State()
#     idioms_collection = State()
users_database = ['alexey']


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_button = ["Ok. Let's begin!"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)
    await message.answer("Hello, " + "*" + message.from_user.first_name +
                         "*! 👋 " + bot_messages.start_message, reply_markup=keyboard)


# @dp.message_handler(lambda message: message.text)
# async def adding_nickname(message: types.Message):
#     start_button = ["Ok. Let's begin!"]
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(*start_button)
#     if message.text not in bot_messages.commands:
#         return await message.reply("Nice! Since now, I know you as *"
#                                    + message.text + "*. Are you ready to begin?",  reply_markup=keyboard)
#     else:
#         return await message.answer("Unfortunately, this nickname has already been taken." +
#                                     " Please create another one.")


@dp.message_handler(Text(equals="Ok. Let's begin!"))
async def first_step(message: types.Message):
    start_buttons = ["Give me an idiom", "Show me the idioms I've saved", "I want to search for an idiom"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*start_buttons)
    # await Form.idiom_example.set()

    await message.answer("Are you ready to _dive into_ idioms?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Give me an idiom"))  # state=Form.idiom_example
async def get_idiom_name(message: types.Message):  # state: FSMContext
    idiom_buttons = ["No. What does it mean?", "I've seen it. Give me another one", "Back to menu"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*idiom_buttons)
    await message.answer("Just a moment. I'm trying to _beat the clock_...")

    random_index = random.randint(0, len(list(data)) - 1)
    global in_d
    in_d = list(data.items())[random_index]
    name = in_d[1].get("idiom_name")
    # async with state.proxy() as datum:
    #     datum['idiom_example'] = in_d
    # await Form.next()

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
    buttons = ["Add this idiom to my collection", "I've seen it. Give me another one", "Back to menu"]
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


@dp.message_handler(lambda message: message.text not in bot_messages.commands)
async def invalid_message(message: types.Message):
    return await message.reply("Later you will be able to search for this. "
                               "But for now, please provide one of current commands")


@dp.message_handler(Text(equals="Add this idiom to my collection"))
async def get_idioms_list(message: types.Message):
    collection_buttons = ["Show me the idioms I've saved", "Back to menu"]
    collection_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    collection_keyboard.add(*collection_buttons)
    await message.answer("Ok, the idiom *" + in_d[1].get("idiom_name")
                         + "* " + "has been saved. "
                                  "Do you want to see your collection or start over?",
                         reply_markup=collection_keyboard)


@dp.message_handler(Text(equals="I've seen it. Give me another one"))
async def go_another(another_message: types.Message):
    await get_idiom_name(another_message)


@dp.message_handler(Text(equals="Show me the idioms I've saved"))
async def get_idioms_list(message: types.Message):
    await message.answer("_Hold your horses_. This function is being developed.")


@dp.message_handler(Text(equals="I want to search for an idiom"))
async def get_idioms_list(message: types.Message):
    await message.answer("Don't _jump the gun_! This function is being developed.")


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()


#  логирование, трейсинг
