from bs4 import BeautifulSoup
# import unicodedata
import requests
import json
# import re
# import time
# import random
import os
headers = {
    "user-agent": \
          "Mozilla / 5.0(Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"+\
              "(KHTML, like Gecko) Chrome/103.0.0.0 Safari / 537.36"
}
iteration_count = 152
print(f"Всего итераций: #{iteration_count}")

for page_number in range(1, 4):
    url_1 = "https://www.theidioms.com/list"
    r = requests.get(url_1 + f"/page/{page_number}/", headers=headers)
    # time.sleep(random.randrange(1, 3))
    folder_name = f"data/data_{page_number}"

    if os.path.exists(folder_name):
        print("Папка уже существует!")
    else:
         os.mkdir(folder_name)

    with open(f"{folder_name}/projects_{page_number}.html", "w") as file:
        file.write(r.text)

    with open(f"{folder_name}/projects_{page_number}.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "xml")
    idiom_url = soup.find_all
    links = []

    # with open("data/links.json", "w") as file:
    #     json.dump(all_links, file, indent=4, ensure_ascii=False)

    for idiom_url in idiom_url('a'):  # чистим ссылки, оставляя только ссылки на фразеологизмы
        if '-' not in idiom_url.get('href') or '#' in idiom_url.get('href'):
            pass
        elif 'privacy-policy' in idiom_url.get('href') or "opposite-words" in idiom_url.get('href'):
            pass
        elif "dig-own-grave" in idiom_url.get('href') or "figure-of-speech" in idiom_url.get('href'):
            pass
        elif "wild-card" in idiom_url.get('href') or "quote-unquote" in idiom_url.get('href'):
            pass
        elif "backhanded-compliment" in idiom_url.get('href') or "end-up" in idiom_url.get('href'):
            pass
        elif "according-to" in idiom_url.get('href') or "arm-to-arm" in idiom_url.get('href'):
            pass
        elif "arm-in-arm" in idiom_url.get('href') or "cut-down" in idiom_url.get('href'):
            pass
        elif "curry-favour" in idiom_url.get('href') or "long-arm-of-the-law" in idiom_url.get('href'):
            pass
        else:
            links.append(idiom_url.get('href'))


    links_set = set(links)  # перевели список во множество, чтобы исключить повторы
    for link in links:
        links_set.add(link)

    all_links = list(links_set)

    with open("data/links.json", "a") as file:
        json.dump(all_links, file, indent=4, ensure_ascii=False)
    # print(links_set)
    print(all_links)
    # print(len(links_set))
    print(len(all_links))