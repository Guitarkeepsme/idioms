from bs4 import BeautifulSoup
import requests
import time
# import json

def get_data(url):
    headers = {
        "user-agent": "Mozilla / 5.0(Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 103.0 .0 .0 Safari / 537.36"
    }
    r = requests.get(url, headers)
    print(r.text)
    with open("projects.html", "w") as file:
        file.write(r.text)

get_data("https://www.theidioms.com/list/#title")
# time.sleep(1.5)
#
# soup = BeautifulSoup(r.text, "html.parser")
# idiom_url = soup.find('div', class_='new-list').find('a')
# links = []
# for idiom_url in soup.find_all('a'):  # почистили список ссылок, оставив только ссылки на фразеологизмы
#     if '-' not in idiom_url.get('href') or '#' in idiom_url.get('href'):
#         pass
#     else:
#         links.append(idiom_url.get('href'))
#
# links_set = set(links)  # переевели список во множество, чтобы исключить повторы
# for link in links:
#     links_set.add(link)
#
# all_data = set()  # закинули все данные в переменную. В дальнейшем необходимая инфа будет передана в json
# for link in list(links_set):
#     url = links_set.pop()
#     response = requests.get(url)
#     time.sleep(1)
#     data = response.content
#     all_data.add(data)

# with open("all_idioms.json", "w") as file:
    # json.dump(list(decode(all_data)), file, indent=4, ensure_ascii=False)
