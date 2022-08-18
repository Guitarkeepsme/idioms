# from googletrans import Translator
#
# translator = Translator()
#
# sample = "Hello, world!"
#
# result = translator.translate("How are you?", dest='ru')
#
# print(result.text)


test_list = ['− armed to the teeth', '− at sea', '− bated breath', '− batten down the hatches', '− blaze a trail',
             '− break a leg', '− break down', '− break open', '− chow down', '− cross the line', '− do justice to',
             '− down the drain', '− drop a bombshell', '− glass ceiling', '− in hand',
             '− its better to be safe than sorry', '− last but not least', '− low hanging fruit',
             '− neck and neck', '− no man is an island', '− old habits die hard', '− on the cards',
             '− one stop shop', '− pull leg', '− recharge ones batteries', '− road to recovery',
             '− shoot from the hip', '− so and so', '− so so', '− speak up', '− take turns',
             '− the pen is mightier than the sword']


def test_function(message):
    if message not in test_list:
        return "Ok"
    else:
        return "Fuck off!"


print(test_function("− neck and neck"))
