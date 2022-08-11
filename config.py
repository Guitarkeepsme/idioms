from enum import Enum

TOKEN="5492669742:AAENd4_UHTbJEpzVIsbiqAKLe_zB3sS_WMQ"
db_file = "database.vdb"


































""" Создать четыре класса:
1) выдача фразеологизма;
2) коллекция фразеологизмов;
3) поиск по базе фразеологизмов;
4) поиск значения слова;
"""


class States(Enum):
    S_START = "0"  # Начало нового диалога
    S_IDIOM = "1"
    S_MEANING = "2"
    S_EXAMPLES = "3"
    S_COLLECTION = "4"
