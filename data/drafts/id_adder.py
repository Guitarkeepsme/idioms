import json


with open("idiom_info.json", encoding='utf-8', newline='') as file:
    data = json.load(file)


counter_id = 1
for line in data.values():
    line.update({"idiom_id": counter_id})
    counter_id = counter_id + 1

with open("../idiom_info_with_id.json", "w", encoding='utf-8', newline='') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
