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


# States
# class Form(StatesGroup):
#     idiom_info = State()


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_button = ["Ok. Let's begin!"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)
    await message.answer("Hello, " + "*" + message.from_user.first_name +
                         "*! 👋" + bot_messages.start_message, reply_markup=keyboard)


@dp.message_handler(Text(equals="Ok. Let's begin!"))
async def first_step(message: types.Message):
    start_buttons = ["Give me an idiom", "Show me the idioms I've saved", "I want to search for an idiom"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(*start_buttons)
    # await Form.idiom_info.set()

    await message.answer("Are you ready to _dive into_ idioms?", reply_markup=keyboard)

# dp.message_handler(lambda message: message.text not in ["Male", "Female", "Other"], state=Form.gender)
# async def process_gender_invalid(message: types.Message):
#    """
#   In this example gender has to be one of: Male, Female, Other.
#   """
# return await message.reply("Bad gender name. Choose your gender from the keyboard.")


@dp.message_handler(lambda message: message.text not in ["Give me an idiom", "Show me the idioms I've saved",
                                                         "I want to search for an idiom",
                                                         "No. What does it mean?", "Show me some examples",
                                                         "I've seen it. Give me another one",
                                                         "Add this idiom to my collection", "Back to menu"])
async def invalid_message(message: types.Message):
    return await message.reply("Later you will be able to search for this word. "
                               + "But for now, provide one of the current commands")


@dp.message_handler(commands='back to menu')
@dp.message_handler(Text(equals="Back to menu", ignore_case=True))
async def go_back(start_message: types.Message): # state: FSMContext
#     # current_state = await state.get_state()
#     # if current_state is None:
#     #     return
    await first_step(start_message)


@dp.message_handler(Text(equals="Give me an idiom")) # state=Form.idiom_info
async def get_idiom_name(message: types.Message): # state: FSMContext
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

    await message.answer("The idiom is " + "*" + str(name) + "*. "
                         + "Have you already seen this one?", reply_markup=keyboard)


@dp.message_handler(Text(equals="No. What does it mean?")) # state=Form.idiom_info
async def get_idiom_meanings(second_message: types.Message): # state: FSMContext
    buttons = ["Show me some examples", "I've seen it. Give me another one", "Back to menu"]
    second_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    second_keyboard.add(*buttons)
    meanings = in_d[1].get("idiom_meaning")

    await second_message.answer("This idiom means: \n \n - " + "_" +
                                str(meanings).replace("END_LINE", "\n \n - ")[0:-3]
                                + "_", reply_markup=second_keyboard)


@dp.message_handler(Text(equals="Show me some examples"))  # state=Form.idiom_info
async def get_idiom_examples(third_message: types.Message):  # state: FSMContext
    buttons = ["Add this idiom to my collection", "I've seen it. Give me another one", "Back to menu"]
    second_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    examples = in_d[1].get("idiom_examples")
    second_keyboard.add(*buttons)
    # попытаться как-то выделить жирным шрифтом идиомы внутри примеров
    # await Form.next()

    await third_message.answer("Here are some examples: \n \n - " + "_" +
                               str(examples).replace("END_LINE", "\n \n - ")[0:-3]
                               + "_", reply_markup=second_keyboard)


# You can use state '*' if you need to handle all states
#  43@dp.message_handler(state='*', commands='cancel')
#  44@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
#  45async def cancel_handler(message: types.Message, state: FSMContext):
#  46    """
#  47    Allow user to cancel any action
#  48    """
#  49    current_state = await state.get_state()
#  50    if current_state is None:
#  51        return
#  52
#  53    logging.info('Cancelling state %r', current_state)
#  54    # Cancel state and inform user about it
#  55    await state.finish()
#  56    # And remove keyboard (just in case)
#  57    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


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

# @dp.message_handler(Text(equals="Give me an idiom"))
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
#             # переписать логику, заменив глобальную переменную на классы -- но потом
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
