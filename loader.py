from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
bot = Bot(token=config.TOKEN, parse_mode="Markdown")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
