from aiogram import types
from aiogram.dispatcher.filters import Text
from data.config import Form, translator
from loader import dp


@dp.message_handler(Text(equals="Translate something"), state=Form.idiom)
async def translate_something(message: types.Message):
    await Form.translation_idiom.set()
    await message.reply("Что вы хотите перевести? Скопируйте и отправьте нужный текст *ответным сообщением*.")


@dp.message_handler(state=Form.translation_idiom)
async def text_to_translate_idiom(message: types.Message):
    translated = translator.translate(message.text, dest='ru')
    await message.reply("*Перевод:* \n\n" + "_" + translated.text + "_")
    await Form.idiom.set()


@dp.message_handler(Text(equals="Translate something"), state=Form.user_idiom)
async def translate_something_user(message: types.Message):
    await Form.translation_idiom_user.set()
    await message.reply("Что вы хотите перевести? Скопируйте и отправьте нужный текст *ответным сообщением*.")


@dp.message_handler(state=Form.translation_idiom_user)
async def text_to_translate_user(message: types.Message):
    translated = translator.translate(message.text, dest='ru')
    await message.reply("*Перевод:* \n\n" + "_" + translated.text + "_")
    await Form.user_idiom.set()


@dp.message_handler(Text(equals="Translate something"), state=Form.confirmation)
async def translate_something_confirmation(message: types.Message):
    await Form.translation_idiom_confirmed.set()
    await message.reply("Что вы хотите перевести? Скопируйте и отправьте нужный текст *ответным сообщением*.")


@dp.message_handler(state=Form.translation_idiom_confirmed)
async def text_to_translate_confirmation(message: types.Message):
    translated = translator.translate(message.text, dest='ru')
    await message.reply("*Перевод:* \n\n" + "_" + translated.text + "_")
    await Form.confirmation.set()


@dp.message_handler(Text(equals="Translate something"), state=Form.idiom_search_adding)
async def translate_something_confirmation(message: types.Message):
    await Form.translation_idiom_from_several.set()
    await message.reply("Что вы хотите перевести? Скопируйте и отправьте нужный текст *ответным сообщением*.")


@dp.message_handler(state=Form.translation_idiom_from_several)
async def text_to_translate_search(message: types.Message):
    translated = translator.translate(message.text, dest='ru')
    await message.reply("*Перевод:* \n\n" + "_" + translated.text + "_")
    await Form.idiom_search_adding.set()