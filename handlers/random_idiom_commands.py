from random import randint

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from data.config import Form, data, cursor, connection


from loader import dp


@dp.message_handler(Text(equals="Ok. Let's begin!"), state=Form.idiom)
async def first_step(message: types.Message):
    start_buttons = ["Give me an idiom", "Show me the idioms I've saved", "I want to search for an idiom"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*start_buttons)

    await message.answer("Are you ready to _dive into_ idioms?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Give me an idiom"), state=Form.idiom)
async def get_idiom_name(message: types.Message, state: FSMContext):
    buttons = ["No. What does it mean?", "I've seen it. Give me another one", "Translate something", "Back to menu"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*buttons)
    random_index = randint(0, len(list(data)) - 1)
    in_d = list(data.items())[random_index]

    async with state.proxy() as current_idiom:
        current_idiom['idiom'] = in_d

    name = in_d[1].get("idiom_name")
    await message.answer("The idiom is " + "*" + str(name) + "*. "
                         + "Have you already seen this one?", reply_markup=keyboard)


@dp.message_handler(Text(equals="No. What does it mean?"), state=Form.idiom)
async def get_idiom_meanings(message: types.Message, state: FSMContext):
    buttons = ["Show me some examples", "I've seen it. Give me another one", "Translate something", "Back to menu"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*buttons)
    async with state.proxy() as current_idiom:
        meanings = current_idiom['idiom'][1].get("idiom_meaning")
        await message.answer("This idiom means: \n \n - " + "_" +
                             str(meanings).replace("END_LINE", "\n \n − ")[0:-3]
                             + "_", reply_markup=keyboard)


@dp.message_handler(Text(equals="Show me some examples"), state=Form.idiom)
async def get_idiom_examples(third_message: types.Message, state: FSMContext):
    buttons = ["Add this idiom to my collection", "I've seen it. Give me another one", "Translate something",
               "Back to menu"]
    second_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    async with state.proxy() as current_idiom:
        examples = current_idiom['idiom'][1].get("idiom_examples")
        second_keyboard.add(*buttons)
        # попытаться как-то выделить жирным шрифтом идиомы внутри примеров
        await third_message.answer("Here are some examples: \n \n − " + "_" +
                                   str(examples).replace("END_LINE", "\n \n − ")[0:-3]
                                   + "_", reply_markup=second_keyboard)


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


@dp.message_handler(Text(equals="I've seen it. Give me another one"), state='*')
async def go_another(message: types.Message, state: FSMContext):
    await Form.idiom.set()
    await get_idiom_name(message, state)
