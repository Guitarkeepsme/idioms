from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from data import bot_messages
from data.config import Form, cursor, connection
from handlers.random_idiom_commands import first_step
from loader import dp


@dp.message_handler(Text(equals="Back to menu"), state='*')
async def go_back(message: types.Message):
    await Form.idiom.set()
    await first_step(message)


@dp.message_handler(Text(equals="Add this idiom to my collection"), state=Form.idiom)
async def update_collection(message: types.Message, state: FSMContext):
    buttons = ["Show me the idioms I've saved", "Translate something", "Back to menu"]
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


@dp.message_handler(Text(equals="Show me the idioms I've saved"), state='*')
async def get_idioms_list(message: types.Message):
    buttons = ["Remind me about an idiom...", "Translate something", "Back to menu"]
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
    await message.answer(bot_messages.reminder, reply_markup=types.ReplyKeyboardRemove())
    await Form.user_idiom.set()


@dp.message_handler(state=Form.user_idiom)
async def idiom_reverse(message: types.Message, state: FSMContext):
    buttons = ["Show me the idioms I've saved", "Translate something", "Back to menu"]
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
    if user_idiom_meaning == []:
        await message.answer("There is no such idiom in your list. Check your message for typos and write again.")
    else:
        await message.answer("*This idiom means:* \n \n" + "_" +
                             str(user_idiom_meaning).replace("END_LINE", "\n \n")[2:-2]
                             + "_" + "*Here are some examples:* \n \n" + "_" +
                             str(user_idiom_examples).replace("END_LINE", "\n \n")[2:-2]
                             + "_", reply_markup=keyboard)

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
