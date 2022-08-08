import sqlite3

connection = sqlite3.connect('Test3.db')
cursor = connection.cursor()
cursor.execute('Create Table if not exists Test3 (id Integer, name Text)')
connection.commit()


dict = {"id": "1", "name": "pruhlesha"}
cursor.execute('INSERT INTO Test3 VALUES (?,?)', [dict['id'], dict['name']])
connection.commit()
# c.execute('insert into tablename values (?,?,?)', [dict['id'], dict['name'], dict['dob']])
