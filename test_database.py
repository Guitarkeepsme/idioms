import json
import sqlite3

connection = sqlite3.connect('idioms.db')
cursor = connection.cursor()
cursor.execute('Create Table if not exists Idiom (idiom_name Text, idiom_meaning Text, idiom_examples Text)')
connection.commit()

data = json.load(open("data/idiom_info.json", encoding='utf-8', newline=''))
columns = ['idiom_name', 'idiom_meaning', 'idiom_examples']
counter = 0
for row in data.values():
    keys = tuple(row[c] for c in columns)
    cursor.execute('INSERT INTO Idiom VALUES (:idiom_name, :idiom_meaning, :idiom_examples)', keys)
    connection.commit()

