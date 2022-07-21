import json
import random
from collections import OrderedDict
with open("data/idiom_info.json") as file:
    data = json.load(file)
# for idiom in data:
#     if idiom is not None:
#         return idiom

test_dic = {"1": {"один": "one"}, "2": {"два": "two"}, "3": {"три": "three"}, "4": {"четыре": "four"}}

test_dic_2 = {
    "to the core": {
        "idiom_name": "to the core",
        "idiom_meaning": "totally;fully;completely;utterly;through and through",
        "idiom_examples": "Stella’s plan was rotten to the core"
    },
    "coin a phrase": {
        "idiom_name": "coin a phrase",
        "idiom_meaning": "as one might say",
        "idiom_examples": "She was, to coin a phrase"
    },
    "sponger sponging sponge off": {
        "idiom_name": "sponger sponging sponge off",
        "idiom_meaning": "someone who scrounges from others",
        "idiom_examples": "Josh has turned up at my house three times this week just as I’m cooking dinner"
    }
}


def idiom_finder(d):
    random_index = random.randint(0, len(list(d)) - 1)
    in_d = list(d.items())[random_index]
    print(in_d[1])
    result = in_d[1].items()
    return result
    # print(in_d[1])


# def poping_idiom(d):
#     d_tmp = d.copy()
#     return d_tmp.popitem()

#
# print(poping_idiom(test_dic))


print(idiom_finder(test_dic_2))