import requests
from bs4 import BeautifulSoup
# import time
# import json

url = "https://www.theidioms.com/list/#title"
r = requests.get(url)
# time.sleep(1.5)

soup = BeautifulSoup(r.text, "html.parser")
idiom_url = soup.find('div', class_='new-list').find('a')
links = []
for idiom_url in soup.find_all('a'):  # почистили список ссылок, оставив только ссылки на фразеологизмы
    if '-' not in idiom_url.get('href') or '#' in idiom_url.get('href'):
        pass
    elif 'privacy-policy' in idiom_url.get('href'):
        pass
    else:
        links.append(idiom_url.get('href'))


links_set = set(links)  # перевели список во множество, чтобы исключить повторы
for link in links:
    links_set.add(link)
# print(links_set)


idiom_content = {}
idiom_examples = {}
for link in links_set:
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    idiom_info = soup.find("div", {"class": "article"})
    idiom_content_tmp = []
    for i in idiom_info.children:
        if "Origin" in i or "Figures of Speech" in i:
            pass
        # for tag in soup.find_all(re.compile("ol")):
        #     idiom_content_tmp.append(tag.string)
        # elif "<ul>" in i or "<li>" in i:
        #     idiom_content_tmp.append(i)
        else:
            idiom_content_tmp.append(i)
    idiom_content[idiom_content_tmp[0]] = {idiom_content_tmp[1]: idiom_content_tmp[2]}
    idiom_examples[idiom_content_tmp[0]] = {idiom_content_tmp[3]: idiom_content_tmp[4]}
print(idiom_content)
print(idiom_examples)


# with open("data/info.json", "a") as file:
#     json.dump(idiom_content, file, indent=4)
