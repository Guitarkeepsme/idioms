from googletrans import Translator

translator = Translator()

sample = "Hello, world!"

result = translator.translate("How are you?", dest='ru')

print(result.text)