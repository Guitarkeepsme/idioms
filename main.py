import unicodedata
import requests
from bs4 import BeautifulSoup
import json
import re
url = "https://www.theidioms.com/list/#title"
r = requests.get(url)
# time.sleep(1.5)

soup = BeautifulSoup(r.text, "html.parser")
idiom_url = soup.find('div', class_='new-list').find('a')
links = []
for idiom_url in soup.find_all('a'):  # чистим ссылки, оставляя только ссылки на фразеологизмы
    if '-' not in idiom_url.get('href') or '#' in idiom_url.get('href'):
        pass
    elif 'privacy-policy' in idiom_url.get('href') or "opposite-words" in idiom_url.get('href'):
        pass
    elif "dig-own-grave" in idiom_url.get('href') or "figure-of-speech" in idiom_url.get('href'):
        pass
    else:
        links.append(idiom_url.get('href'))


links_set = set(links)  # перевели список во множество, чтобы исключить повторы
for link in links:
    links_set.add(link)
# print(links_set)


# def merge(dict_1, dict_2):
#     result = dict_1 | dict_2
#     return result


idiom_content = {}
idiom_examples = {}
for link in links_set:
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    idiom_info = soup.find("div", {"class": "article"})
    idiom_content_tmp = []
    idiom_content_without_tags = []
    for i in idiom_info.children:
        if "Origin" in i:
            break
        else:
            idiom_content_tmp.append(i)

    for item in idiom_content_tmp:
        bar = re.sub("<[^>]*>", " ", unicodedata.normalize("NFKD", str(item)))
        idiom_content_without_tags.append(bar)
    print(idiom_content_without_tags)
    # idiom_content[idiom_content_without_tags[0]] = {idiom_content_without_tags[1]: idiom_content_without_tags[2]},\
    #                                                {idiom_content_without_tags[3]: idiom_content_without_tags[4]}
    idiom_content[idiom_content_without_tags[0]] = {idiom_content_without_tags[2]: idiom_content_without_tags[4]}
# idiom_all_info = merge(idiom_examples, idiom_content)

print(idiom_content)
# print(idiom_examples)
# print(idiom_all_info)


with open("data/idiom_info.json", "a") as file:
    json.dump(idiom_content, file, indent=4)
