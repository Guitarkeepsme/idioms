from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from data import bot_messages
from data.config import Form, data, levenshtein, cursor, connection
from handlers.random_idiom_commands import first_step
from loader import dp


@dp.message_handler(Text(equals="Back to menu"), state='*')
async def go_back(message: types.Message):
    await Form.idiom.set()
    await first_step(message)


@dp.message_handler(Text(equals="I want to search for an idiom"), state='*')
async def idiom_search_message(message: types.Message):
    button = ["Back to menu"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*button)
    await message.answer(bot_messages.idiom_search_message, reply_markup=keyboard)
    await Form.idiom_search.set()


@dp.message_handler(state=Form.idiom_search)
async def idiom_search(message: types.Message, state: FSMContext):
    buttons = ["Add this idiom to my collection", "Translate something", "Back to menu"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*buttons)
    right_idiom_counter = 0
    idiom_collection = []
    for idiom in data:
        if levenshtein.distance(idiom, message.text) > 4:
            continue
        else:
            right_idiom_counter += 1
            idiom_collection.append(idiom)
    if right_idiom_counter > 1:
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
        await Form.idiom_search_several.set()
    elif right_idiom_counter == 0:
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
        buttons = ["Add this idiom to my collection", "Translate something", "Back to menu"]
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
            await Form.idiom_search_adding.set()
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


@dp.message_handler(state=Form.idiom_search_several)
async def picking_idiom(message: types.Message, state: FSMContext):
    lower_message = message.text.lower()
    buttons = ["Add this idiom to my collection", "Translate something", "Back to menu"]
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
        await Form.idiom_search_adding.set()

        async with state.proxy() as searched_idiom:
            searched_idiom["searched_idiom"] = message.text

        await message.answer("The idiom *" + message.text + "* means: \n\n "
                             + "_" +
                             str(idiom_meaning).replace("END_LINE", "\n \n ")[2:-3]
                             + "_" + "*Here are some examples:* \n \n" + "_" +
                             str(idiom_examples).replace("END_LINE", "\n \n")[2:-2]
                             + "_", reply_markup=keyboard)


@dp.message_handler(Text(equals="Add this idiom to my collection"), state=Form.idiom_search_adding)
async def update_collection_after_search(message: types.Message, state: FSMContext):
    buttons = ["Show me the idioms I've saved", "Translate something", "Back to menu"]
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