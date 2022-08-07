import sqlite3
import json


conn = sqlite3.connect('idioms.db')
cursor = conn.cursor()
cursor.execute('Create Table if not exists Idiom (idiom_name Text, idiom_meaning Text, idiom_examples Text)')

data = json.load(open("data/idiom_info.json", encoding='utf-8', newline=''))
columns = ['idiom_name', 'idiom_meaning', 'idiom_examples']
counter = 0
for row in data.values():
    keys = tuple(row[c] for c in columns)
    cursor.execute('insert into Idiom values(?,?,?)', keys)
    # print(f'{row["name"]} data inserted Succesfully')
    counter += 1
    if counter == 10:
        break


# def table_exists(table_name):
#     c.execute('''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = '{}' '''.format(table_name))
#     if c.fetchone()[0] == 1:
#         return True
#     return False
#
#
# if not table_exists('idioms'):
#     c.execute('''
#         CREATE TABLE idioms(
#             idiom_id INTEGER,
#             name TEXT
#         )
#     ''')


# def insert_idiom(idiom_id, name):
#     c.execute(''' INSERT INTO idioms (idiom_id, name) VALUES(?, ?) ''',
#               (idiom_id, name))
#     conn.commit()


# import json
# import sqlite3
#
# connection = sqlite3.connect('db.sqlite')
# cursor = connection.cursor()
# cursor.execute('Create Table if not exists Student (name Text, course Text, roll Integer)')
#
# traffic = json.load(open('json_file.json'))
# columns = ['name','course','roll']
# for row in traffic:
#     keys= tuple(row[c] for c in columns)
#     cursor.execute('insert into Student values(?,?,?)',keys)
#     print(f'{row["name"]} data inserted Succesfully')
#
# connection.commit()
# connection.close()
