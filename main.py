from bs4 import BeautifulSoup
import unicodedata
import requests
import json
import re
# import time
# import random

all_links = []
iteration_count = 152
print(f"Всего обходов: {iteration_count}")

for page_number in range(1, 152):
    url = "https://www.theidioms.com/list"
    r = requests.get(url + f"/page/{page_number}/")
    # time.sleep(random.randrange(1, 3))

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
        elif "blood-sweat-and-tears" in idiom_url.get("href"):
            pass
        else:
            links.append(idiom_url.get('href'))
        # это временная мера. Позже исправлю проблему, возникающую при большом количестве примеров предложений

    all_links.extend(links)
    all_links_set = set(all_links)  # перевели список во множество, чтобы исключить повторы

    for link in all_links:
        all_links_set.add(link)
    idiom_content = {}
    for link in all_links_set:
        r = requests.get(link)
        soup = BeautifulSoup(r.text, "lxml")
        idiom_info = soup.find("div", {"classgit": "article"})
        idiom_content_tmp = []
        idiom_content_without_tags = []
        for i in idiom_info.children:
            # на этом этапе необходимо распределить инфу в соответствии с тэгами
            # один тэг для значений, другой для примеров
            # не забыть ограничить количество оных до пяти включительно
            if "Origin" in i:
                break
            else:
                idiom_content_tmp.append(i)
        for item in idiom_content_tmp:
            bar = str(item).replace("</li>", "\n")  # replace("<strong>", "**").replace("</strong>", "**")
            with_n_bar = re.sub("<[^>]*>", " ", unicodedata.normalize("NFKD", bar))
            idiom_content_without_tags.append(with_n_bar.strip())
        idiom_name = link.split(".com/")[-1].replace("/", "").replace("-", " ")
        # print(idiom_name)
        idiom_content[idiom_name] = {
            "idiom_name": idiom_content_without_tags[0],
            "idiom_meaning": idiom_content_without_tags[2].replace("  ", " "),
            "idiom_examples": idiom_content_without_tags[4].replace("   ", " ").replace("  ", " ")
        }
        # print(idiom_content)


        with open("data/idiom_info.json", "w") as file:
            json.dump(idiom_content, file, indent=4, ensure_ascii=False)
    iteration_count -= 1
    print(f"Обход №{page_number} завершён, осталось обходов: {iteration_count}")
    if iteration_count == 0:
        print("Сбор данных завершен")