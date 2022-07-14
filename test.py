import re

Foo = ["KeyboardEvent(enter up)", "KeyboardEvent(h down)", "KeyboardEvent(h up)"]
Foo1 = ["<p><strong>sell like hot cakes</strong></p>", "<h2>Meaning</h2>", "<ul><li>be a great commercial success</li><li>to dispose </li>"]

strList = []

for item in Foo1:
    bar = re.sub("<[^>]*>", "", str(item))
    strList.append(bar)


# for item in Foo1:
#     bar = re.sub('KeyboardEvent(\(.*?)', '', str(item))
#     bar = re.sub('\)', '', bar)
#     strList.append(bar)
print(strList)
