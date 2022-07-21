from aiogram import Bot, Dispatcher, executor, types
# import os
from aiogram.dispatcher.filters import Text
import json
import random


bot = Bot(token="5492669742:AAENd4_UHTbJEpzVIsbiqAKLe_zB3sS_WMQ", parse_mode="Markdown")
# bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Give me an idiom", "Open saved idioms", "Find an idiom"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Hello! Let's get started?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Give me an idiom"))
async def get_idiom_name(message: types.Message):
    idiom_buttons = ["What does it mean?", "Give another one", "Back to menu"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*idiom_buttons)
    await message.answer("Just a moment. I'm trying to _beat the clock_...")

    with open("data/idiom_info.json") as file:
        data = json.load(file)
        random_index = random.randint(0, len(list(data)) - 1)
        in_d = list(data.items())[random_index]
        name = in_d[1].get("idiom_name")
        await message.answer("The idiom is " + "*" + str(name) + "*", reply_markup=keyboard)

        @dp.message_handler(Text(equals="What does it mean?"))
        async def get_idiom_meanings(second_message: types.Message):
            buttons = ["Show examples", "Give me another idiom"] + \
                    ["Back to menu"]
            second_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            second_keyboard.add(*buttons)
            meanings = in_d[1].get("idiom_meaning")

            await second_message.answer("This idiom means: \n \n - " + "_" +
                                        str(meanings).replace("END_LINE", "\n \n - ")[0:-3]
                                        + "_", reply_markup=second_keyboard)

        @dp.message_handler(Text(equals="Show examples"))
        async def get_idiom_examples(third_message: types.Message):
            buttons = ["Back to menu"] + \
                      ["Give me another idiom", "Add to my list"]
            second_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            second_keyboard.add(*buttons)
            examples = in_d[1].get("idiom_examples")
            # попытаться как-то выделить жирным шрифтом идиомы внутри примеров
            await third_message.answer("Here are some examples: \n \n - " + "_" +
                                       str(examples).replace("END_LINE", "\n \n - ")[0:-3]
                                       + "_", reply_markup=second_keyboard)

        @dp.message_handler(Text(equals="Give another one"))
        async def get_another_idiom(message: types.Message):
            idiom_buttons = ["What does it mean?", "Give another one", "Back to menu"]
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*idiom_buttons)

            with open("data/idiom_info.json") as file:
                data = json.load(file)
                second_random_index = random.randint(0, len(list(data)) - 1)
                in_d = list(data.items())[second_random_index]
                name = in_d[1].get("idiom_name")
                await message.answer("The idiom is " + "*" + str(name) + "*", reply_markup=keyboard)

                @dp.message_handler(Text(equals="What does it mean?"))
                async def get_another_meanings(second_message: types.Message):
                    buttons = ["Show examples", "Give me another idiom"] + \
                              ["Back to menu"]
                    second_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    second_keyboard.add(*buttons)
                    meanings = in_d[1].get("idiom_meaning")

                    await second_message.answer("This idiom means: \n \n - " + "_" +
                                                str(meanings).replace("END_LINE", "\n \n - ")[0:-3]
                                                + "_", reply_markup=second_keyboard)

                @dp.message_handler(Text(equals="Show examples"))
                async def get_another_examples(third_message: types.Message):
                    buttons = ["Back to menu"] + \
                              ["Give me another idiom", "Add to my list"]
                    second_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    second_keyboard.add(*buttons)
                    examples = in_d[1].get("idiom_examples")
                    # попытаться как-то выделить жирным шрифтом идиомы внутри примеров
                    await third_message.answer("Here are some examples: \n \n - " + "_" +
                                               str(examples).replace("END_LINE", "\n \n - ")[0:-3]
                                               + "_", reply_markup=second_keyboard)


@dp.message_handler(Text(equals="Open saved idioms"))
async def get_idioms_list(message: types.Message):
    await message.answer("_Hold your horses_. This function is being developed")


@dp.message_handler(Text(equals="Find an idiom"))
async def get_idioms_list(message: types.Message):
    await message.answer("_Hold your horses_. This function is being developed")


@dp.message_handler(Text(equals="Add to my list"))
async def get_idioms_list(message: types.Message):
    await message.answer("_Hold your horses_. This function is being developed")



def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
