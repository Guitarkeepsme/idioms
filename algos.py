from strsimpy.levenshtein import Levenshtein

levenshtein = Levenshtein()
print(levenshtein.distance('My string', 'My $string'))
print(levenshtein.distance('My string', 'My $sasdtring'))
print(levenshtein.distance('My string', 'My $string'))

"""ПОЛЬЗОВАТЕЛЬ ПИШЕТ КАКУЮ-ТО ИДИОМУ. В СЛУЧАЕ ЕСЛИ РАССТОЯНИЕ ЛЕВЕНШТЕЙНА РАВНО НУЛЮ, ЕМУ ВЫДАЁТСЯ
ЭТА ИДИОМА. В ПРОТИВНОМ СЛУЧАЕ ПРЕДЛАГАЮТСЯ ВАРИАНТЫ С РАССТРОЯНИЕМ ДО ПЯТИ"""

