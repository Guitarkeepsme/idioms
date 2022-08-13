import json
import sqlite3

connection = sqlite3.connect('data/idioms.db')
cursor = connection.cursor()
cursor.execute('Create Table if not exists Idioms '
               '(idiom_name TEXT, idiom_meaning TEXT, idiom_examples TEXT, idiom_id INTEGER PRIMARY KEY)')
connection.commit()

data = json.load(open("data/idiom_info_with_id.json", encoding='utf-8', newline=''))
columns = ['idiom_name', 'idiom_meaning', 'idiom_examples', 'idiom_id']
for row in data.values():
    keys = tuple(row[c] for c in columns)
    cursor.execute('INSERT OR IGNORE INTO Idioms VALUES (?, ?, ?, ?)', keys)
    connection.commit()


cursor.execute('Create Table if not exists Idiom_collections (User_id TEXT, idiom_id INTEGER)')
connection.commit()


cursor.execute('Create Table if not exists Users (ID Text PRIMARY KEY)')
connection.commit()