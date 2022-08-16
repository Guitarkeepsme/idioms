from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import json
import random
import config
import sqlite3
from data import bot_messages
from strsimpy.levenshtein import Levenshtein


bot = Bot(token=config.TOKEN, parse_mode="Markdown")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
levenshtein = Levenshtein()

with open("data/idiom_info_with_id.json", encoding='utf-8', newline='') as file:
    data = json.load(file)


connection = sqlite3.connect('data/idioms.db')
cursor = connection.cursor()


class Form(StatesGroup):
    idiom = State()
    user_idiom = State()
    idiom_search = State()
    idiom_search_2 = State()
    idiom_search_3 = State()
    confirmation = State()
    # delete_idiom = State()


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


@dp.message_handler(Text(equals="Ok. Let's begin!"), state=Form.idiom)
async def first_step(message: types.Message):
    start_buttons = ["Give me an idiom", "Show me the idioms I've saved", "I want to search for an idiom"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*start_buttons)

    await message.answer("Are you ready to _dive into_ idioms?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Give me an idiom"), state=Form.idiom)
async def get_idiom_name(message: types.Message, state: FSMContext):
    buttons = ["No. What does it mean?", "I've seen it. Give me another one", "Back to menu"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*buttons)
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
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*buttons)
    async with state.proxy() as current_idiom:
        meanings = current_idiom['idiom'][1].get("idiom_meaning")
        await message.answer("This idiom means: \n \n - " + "_" +
                             str(meanings).replace("END_LINE", "\n \n − ")[0:-3]
                             + "_", reply_markup=keyboard)


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
    buttons = ["Show me the idioms I've saved", "Back to menu"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*buttons)
    async with state.proxy() as current_idiom:
        idiom_name = current_idiom["idiom"][1].get("idiom_name")
        idiom_id = current_idiom["idiom"][1].get("idiom_id")
        cursor.execute('INSERT INTO Idiom_collections (User_id, Idiom_id) VALUES (?, ?)',
                       (message.from_user.id, idiom_id))
        connection.commit()
        await message.answer("Ok, the idiom *" + idiom_name
                             + "* " + "has been saved. Do you want to see your collection or start over?",
                             reply_markup=keyboard)


@dp.message_handler(Text(equals="I've seen it. Give me another one"), state='*')
async def go_another(message: types.Message, state: FSMContext):
    await Form.idiom.set()
    await get_idiom_name(message, state)


@dp.message_handler(Text(equals="Back to menu"), state='*')
async def go_back(message: types.Message):
    await Form.idiom.set()
    await first_step(message)


@dp.message_handler(Text(equals="Show me the idioms I've saved"), state='*')
async def get_idioms_list(message: types.Message):
    buttons = ["Remind me about an idiom...", "Back to menu"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*buttons)
    cursor.execute('SELECT idiom_name FROM Idioms WHERE idiom_id in'
                   ' (SELECT idiom_id FROM Idiom_collections WHERE User_id = ?)', (message.from_user.id,))
    idioms_list = cursor.fetchall()
    connection.commit()
    result = []
    for idiom in idioms_list:
        str_idiom = "−" + " " + " ".join(idiom)
        result.append(str_idiom)
    result.sort(reverse=False)
    await Form.idiom.set()
    await message.answer("*Your idioms are:* \n " + str(result).replace("'", "\n").replace(",", " ") +
                         "\n \n Do you want me to *remind* you about an idiom or start over?",
                         reply_markup=keyboard)


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
    user_idiom_meaning = [item[0] for item in cursor.fetchall()]
    connection.commit()
    cursor.execute('SELECT idiom_examples FROM Idioms WHERE idiom_name = ?', (message.text,))
    user_idiom_examples = [item[0] for item in cursor.fetchall()]
    connection.commit()
    # print(user_idiom)
    if user_idiom_meaning == []:
        await message.answer("There is no such idiom in your list. Check your message for typos and write again.")
    else:
        await message.answer("*This idiom means:* \n \n" + "_" +
                             str(user_idiom_meaning).replace("END_LINE", "\n \n")[2:-2]
                             + "_" + "*Here are some examples:* \n \n" + "_" +
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
async def idiom_search_message(message: types.Message):
    button = ["Back to menu"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*button)
    await message.answer(bot_messages.idiom_search_message, reply_markup=keyboard)
    await Form.idiom_search.set()


# @dp.message_handler(state=Form.idiom_search)
# async def idiom_search(message: types.message):
#     buttons = ["Back to menu"]
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     keyboard.add(*buttons)
#     await message.answer("_Get yourself together!_ The function is being developed.", reply_markup=keyboard)


@dp.message_handler(state=Form.idiom_search)
async def idiom_search(message: types.Message, state: FSMContext):
    buttons = ["Add this idiom to my collection", "Back to menu"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*buttons)
    idiom_counter = 0  # total amount if idioms in the base is 1387, so we will you this number
    right_idiom_counter = 0
    idiom_collection = []
    for idiom in data:
        if levenshtein.distance(idiom, message.text) > 4:
            idiom_counter += 1
        else:
            right_idiom_counter += 1
            idiom_collection.append(idiom)
    if right_idiom_counter != 1:
        back_button = ["Back to menu"]
        back_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_keyboard.add(*back_button)
        # print(idiom_collection)
        result = []
        for idiom in idiom_collection:
            str_idiom = "−" + " " + "".join(idiom)
            result.append(str_idiom)
        result.sort(reverse=False)
        await message.answer("I have found several idioms. There are: \n" +
                             str(result).replace("'", "\n").replace(",", " ") +
                             "\n\nPlease choose one of them.", reply_markup=back_keyboard)
        await Form.idiom_search_2.set()
    elif idiom_counter == 1387:
        await message.answer("There is no such idiom. Please try again and be just a bit more precise.")
    else:
        conf_buttons = ["Yes", "No", "Back to menu"]
        conf_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        conf_keyboard.add(*conf_buttons)

        async with state.proxy() as searched_idiom:
            searched_idiom["searched_idiom"] = idiom_collection[0]

        await Form.confirmation.set()
        await message.answer("Did you mean the idiom * " + idiom_collection[0] + "?*", reply_markup=conf_keyboard)


@dp.message_handler(state=Form.confirmation)
async def confirmation(message: types.Message, state: FSMContext):
    if message.text == "Yes":
        buttons = ["Add this idiom to my collection", "Back to menu"]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        keyboard.add(*buttons)
        async with state.proxy() as searched_idiom:
            idiom_name = searched_idiom['searched_idiom']
            cursor.execute('SELECT idiom_meaning FROM Idioms WHERE idiom_name = ?', (idiom_name,))
            idiom_meaning = [item[0] for item in cursor.fetchall()]
            connection.commit()
            cursor.execute('SELECT idiom_examples FROM Idioms WHERE idiom_name = ?', (idiom_name,))
            idiom_examples = [item[0] for item in cursor.fetchall()]
            connection.commit()
            await Form.idiom_search_3.set()
            await message.answer("Ok, the idiom *" + idiom_name + "* means:\n\n "
                                 + "_" +
                                 str(idiom_meaning).replace("END_LINE", "\n \n ")[2:-3]
                                 + "_" + "*Here are some examples:* \n \n" + "_" +
                                 str(idiom_examples).replace("END_LINE", "\n \n")[2:-2]
                                 + "_" + "\n*Do you want to save it or start over?*", reply_markup=keyboard)
    elif message.text == "No":
        await message.answer("Ok, let's try again.", reply_markup=types.ReplyKeyboardRemove())
        await Form.idiom_search.set()
        await idiom_search_message(message)


@dp.message_handler(state=Form.idiom_search_2)
async def picking_idiom(message: types.Message, state: FSMContext):
    lower_message = message.text.lower()
    buttons = ["Add this idiom to my collection", "Back to menu"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*buttons)
    cursor.execute('SELECT idiom_meaning FROM Idioms WHERE idiom_name = ?', (lower_message,))
    idiom_meaning = [item[0] for item in cursor.fetchall()]
    connection.commit()
    cursor.execute('SELECT idiom_examples FROM Idioms WHERE idiom_name = ?', (lower_message,))
    idiom_examples = [item[0] for item in cursor.fetchall()]
    connection.commit()
    if idiom_meaning == []:
        await message.answer("Make sure you didn't make any typos and try again.")
    else:
        await Form.idiom_search_3.set()

        async with state.proxy() as searched_idiom:
            searched_idiom["searched_idiom"] = message.text

        await message.answer("The idiom *" + message.text + "* means: \n\n "
                         + "_" +
                         str(idiom_meaning).replace("END_LINE", "\n \n ")[2:-3]
                         + "_" + "*Here are some examples:* \n \n" + "_" +
                         str(idiom_examples).replace("END_LINE", "\n \n")[2:-2]
                         + "_", reply_markup=keyboard)


@dp.message_handler(Text(equals="Add this idiom to my collection"), state=Form.idiom_search_3)
async def update_collection_after_search(message: types.Message, state: FSMContext):
    buttons = ["Show me the idioms I've saved", "Back to menu"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*buttons)
    async with state.proxy() as searched_idiom:
        idiom_name = searched_idiom["searched_idiom"]
        idiom_id = data[idiom_name].get("idiom_id")
        cursor.execute('INSERT INTO Idiom_collections (User_id, Idiom_id) VALUES (?, ?)',
                       (message.from_user.id, idiom_id))
        connection.commit()
        await message.answer("Ok, the idiom *" + idiom_name
                             + "* " + "has been saved. Do you want to see your collection or start over?",
                             reply_markup=keyboard)


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()


#  логирование, трейсинг, ttd
