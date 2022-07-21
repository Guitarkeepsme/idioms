import json

with open("data/idiom_info.json") as file:
    data = json.load(file)
# for idiom in data:
#     if idiom is not None:
#         return idiom

test_dic = {"1": {"один": "one"}, "2": {"два": "two"}, "3": {"три": "three"}}


def sort_dic(d):
    for key in d:
        inside_d = d.get(key)
        for in_key in inside_d:
            print(inside_d.get(in_key))


sort_dic(test_dic)


