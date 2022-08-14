from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
# import aiogram.utils.markdown as md
from aiogram.dispatcher import FSMContext
import json
import random
import config
import sqlite3
# import asyncio
from data import bot_messages
bot = Bot(token=config.TOKEN, parse_mode="Markdown")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


with open("data/idiom_info_with_id.json", encoding='utf-8', newline='') as file:
    data = json.load(file)


connection = sqlite3.connect('data/idioms.db')
cursor = connection.cursor()


class Form(StatesGroup):
    idiom = State()
    user_idiom = State()
    # delete_idiom = State()


@dp.message_handler(commands="start", state='*')
async def start(message: types.Message):
    start_button = ["Ok. Let's begin!"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)
    cursor.execute('INSERT OR IGNORE INTO Users (ID) VALUES (:ID)', (message.from_user.username,))
    connection.commit()
    await message.answer("Hello, " + "*" + message.from_user.first_name +
                         "*! 👋 " + bot_messages.start_message, reply_markup=keyboard)


# @dp.message_handler(commands=["reset"])
# def cmd_reset(message: types.Message):
#     start_button = ["Ok. Let's begin!"]
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(*start_button)
#     dbworker.set_state(message.chat.id, config.States.S_IDIOM.value)
#     await message.answer("Well, let's start _from scratch_. \n\n\n Hello, " + "*" + message.from_user.first_name +
#                          "*! 👋 " + bot_messages.start_message, reply_markup=keyboard)


@dp.message_handler(Text(equals="Ok. Let's begin!"), state='*')
async def first_step(message: types.Message):
    start_buttons = ["Give me an idiom", "Show me the idioms I've saved", "I want to search for an idiom"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*start_buttons)
    await Form.idiom.set()
    # dbworker.set_state(message.chat.id, config.States.S_IDIOM.value)

    await message.answer("Are you ready to _dive into_ idioms?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Give me an idiom"), state=Form.idiom)
#  lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_IDIOM.value
async def get_idiom_name(message: types.Message, state: FSMContext):
    idiom_buttons = ["No. What does it mean?", "I've seen it. Give me another one", "Back to menu"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*idiom_buttons)
    await message.answer("Just a moment. I'm trying to _beat the clock_...")

    random_index = random.randint(0, len(list(data)) - 1)
    in_d = list(data.items())[random_index]

    async with state.proxy() as current_idiom:
        current_idiom['idiom'] = in_d
    name = in_d[1].get("idiom_name")

    await message.answer("The idiom is " + "*" + str(name) + "*. "
                         + "Have you already seen this one?", reply_markup=keyboard)


@dp.message_handler(Text(equals="No. What does it mean?"), state=Form.idiom)
async def get_idiom_meanings(message: types.Message, state: FSMContext):
    buttons = ["Show me some examples", "I've seen it. Give me another one", "Back to menu"]
    second_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    second_keyboard.add(*buttons)
    async with state.proxy() as current_idiom:
        meanings = current_idiom['idiom'][1].get("idiom_meaning")
        await message.answer("This idiom means: \n \n - " + "_" +
                             str(meanings).replace("END_LINE", "\n \n − ")[0:-3]
                             + "_", reply_markup=second_keyboard)


@dp.message_handler(Text(equals="Show me some examples"), state=Form.idiom)
async def get_idiom_examples(third_message: types.Message, state: FSMContext):
    buttons = ["Add this idiom to my collection", "I've seen it. Give me another one", "Back to menu"]
    second_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    async with state.proxy() as current_idiom:
        examples = current_idiom['idiom'][1].get("idiom_examples")
        second_keyboard.add(*buttons)
        # попытаться как-то выделить жирным шрифтом идиомы внутри примеров
        await third_message.answer("Here are some examples: \n \n − " + "_" +
                                   str(examples).replace("END_LINE", "\n \n − ")[0:-3]
                                   + "_", reply_markup=second_keyboard)


@dp.message_handler(lambda message: message.text not in bot_messages.commands, state=Form.idiom)
async def invalid_message(message: types.Message):
    return await message.reply("Later you will be able to search for this. "
                               "But for now, please provide one of current commands. \n\n"
                               "If you wanted to *remind you about an idiom*, click the keyboard button first.")


@dp.message_handler(Text(equals="Add this idiom to my collection"), state=Form.idiom)
async def update_collection(message: types.Message, state: FSMContext):
    collection_buttons = ["Show me the idioms I've saved", "Back to menu"]
    collection_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    collection_keyboard.add(*collection_buttons)
    async with state.proxy() as current_idiom:
        idiom_name = current_idiom["idiom"][1].get("idiom_name")
        idiom_id = current_idiom["idiom"][1].get("idiom_id")
        cursor.execute('INSERT INTO Idiom_collections (User_id, Idiom_id) VALUES (?, ?)',
                       (message.from_user.username, idiom_id))
        connection.commit()
        await message.answer("Ok, the idiom *" + idiom_name
                             + "* " + "has been saved. Do you want to see your collection or start over?",
                             reply_markup=collection_keyboard)


@dp.message_handler(Text(equals="I've seen it. Give me another one"), state='*')
async def go_another(another_message: types.Message, state: FSMContext):
    await Form.idiom.set()
    await get_idiom_name(another_message, state)


@dp.message_handler(Text(equals="Back to menu"), state='*')
async def go_back(start_message: types.Message):
    await first_step(start_message)


@dp.message_handler(Text(equals="Show me the idioms I've saved"), state='*')
async def get_idioms_list(message: types.Message):
    collection_buttons = ["Remind me about an idiom...", "Back to menu"]
    collection_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    collection_keyboard.add(*collection_buttons)
    cursor.execute('SELECT idiom_name FROM Idioms WHERE idiom_id in'
                   ' (SELECT idiom_id FROM Idiom_collections WHERE User_id = ?)', (message.from_user.username,))
    idioms_list = cursor.fetchall()
    connection.commit()
    result = []
    for idiom in idioms_list:
        str_idiom = "−" + " " + " ".join(idiom)
        result.append(str_idiom)
    result.reverse()
    await message.answer("*Your idioms are:* \n " + str(result).replace("'", "\n").replace(",", " ") +
                         "\n \n Do you want me to *remind* you about an idiom or *delete* one of them?",
                         reply_markup=collection_keyboard)


@dp.message_handler(Text(equals="Remind me about an idiom..."), state=Form.idiom)
async def reminder_message(message: types.Message):
    await message.answer(bot_messages.reminder)
    await Form.user_idiom.set()


@dp.message_handler(state=Form.user_idiom)
async def idiom_reverse(message: types.Message, state: FSMContext):
    buttons = ["Show me the idioms I've saved", "Back to menu"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*buttons)
    async with state.proxy() as user_idiom_name:
        user_idiom_name['user_idiom'] = message.text
    cursor.execute('SELECT idiom_meaning FROM Idioms WHERE idiom_name = ?', (message.text,))
    user_idiom = [item[0] for item in cursor.fetchall()]
    connection.commit()
    cursor.execute('SELECT idiom_examples FROM Idioms WHERE idiom_name = ?', (message.text,))
    user_idiom_examples = [item[0] for item in cursor.fetchall()]
    connection.commit()
    print(user_idiom)
    if user_idiom == []:
        await message.answer("There is no such idiom in your list. Check your message for typos and write again.")
    else:
        await message.answer("*This idiom means:* \n \n" + "_" +
                             str(user_idiom).replace("END_LINE", "\n \n")[2:-2]
                             + "_" + "*Here are some examples:* \n \n " + "_" +
                             str(user_idiom_examples).replace("END_LINE", "\n \n")[2:-2]
                             + "_", reply_markup=keyboard)
        # await Form.delete_idiom.set()
    # добавить дефисы в начале строк


# @dp.message_handler(Text(equals="Delete this idiom from my collection"), state=Form.delete_idiom)
# async def delete_this_idiom(message: types.Message):
#     buttons = ["Yes, delete it", "No, back to menu"]
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     keyboard.add(*buttons)
#     await message.answer("Are you sure you want to _get rid of_ this idiom?", reply_markup=keyboard)
#
#     @dp.message_handler(state=Form.delete_idiom)
#     async def confirming_delete(second_message: types.Message):
#         if second_message.text == "Yes, delete it":
#             await second_message.answer("Ok, it has been deleted.")
#         else:
#             await first_step(second_message)


@dp.message_handler(Text(equals="I want to search for an idiom"), state='*')
async def get_idioms_list(message: types.Message):
    await message.answer("Don't _jump the gun_! This function is being developed.")


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()


#  логирование, трейсинг


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
