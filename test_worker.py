# import json
# from strsimpy.levenshtein import Levenshtein
# import sqlite3
#
# with open("data/idiom_info.json", encoding='utf-8', newline='') as file:
#     data = json.load(file)
#
# connection = sqlite3.connect('data/idioms.db')
# cursor = connection.cursor()
#
# levenshtein = Levenshtein()
# test_message = "still waters run dep"
#
#
# def test_1(d):
#     result = []
#     for idiom in d:
#         if levenshtein.distance(idiom, test_message) < 5:
#             cursor.execute('SELECT idiom_meaning FROM Idioms WHERE idiom_name = ?', (idiom,))
#             user_idiom = [item[0] for item in cursor.fetchall()]
#             connection.commit()
#             result.append(user_idiom)
#         else:
#             continue
#     return result
#
# print(test_1(data))


idiom_counter = []
print(len(idiom_counter))
