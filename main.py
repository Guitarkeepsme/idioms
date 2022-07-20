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

    soup = BeautifulSoup(r.text, "lxml")
    links = []
    for idiom_url in soup.find_all('a'):  # чистим ссылки, оставляя только ссылки на фразеологизмы
        if '-' not in idiom_url.get('href') or '#' in idiom_url.get('href'):
            pass
        elif "privacy-policy" in idiom_url.get('href') or "opposite-words" in idiom_url.get('href'):
            pass
        elif "have-designs-on" in idiom_url.get('href') or "figure-of-speech" in idiom_url.get('href'):
            pass
        elif "according-to" in idiom_url.get('href') or "quote-unquote" in idiom_url.get('href'):
            pass
        elif "dig-own-grave" in idiom_url.get('href') or "red-book" in idiom_url.get('href'):
            pass
        else:
            links.append(idiom_url.get('href'))
        # вычеркнул то, что не относится к фразеологизмам, а также те страницы, где расставлены неверные тэги

    all_links.extend(links)
    all_links_set = set(all_links)  # перевели список во множество, чтобы исключить повторы
    print(links)
    for link in all_links:
        all_links_set.add(link)
    idiom_content = {}
    for link in all_links_set:
        r = requests.get(link)
        soup = BeautifulSoup(r.text, "lxml")
        idiom_info = soup.find("div", {"class": "article"})
        meanings_soup = idiom_info.find("ul")
        sentences_soup = idiom_info.find("ol")
        # idiom_content_tmp = []
        # idiom_content_without_tags = []
        meanings = []
        sentences = []
        meanings_counter = 0
        sentences_counter = 0
        for phrase in meanings_soup:
            bar = str(phrase).replace("</li>", ";")  # replace("<strong>", "**").replace("</strong>", "**")
            with_n_bar = re.sub("<[^>]*>", " ", unicodedata.normalize("NFKD", bar))
            meanings.append(with_n_bar.replace("   ", " ").replace("  ", " ").replace(".", ""))
            meanings_counter += 1
            if meanings_counter == 5:
                break
        for example in sentences_soup:
            bar = str(example).replace("</li>", "")  # replace("<strong>", "**").replace("</strong>", "**")
            with_n_bar = re.sub("<[^>]*>", " ", unicodedata.normalize("NFKD", bar))
            sentences.append(with_n_bar.replace("   ", " ").replace("  ", " "))
            sentences_counter += 1
            if sentences_counter == 5:
                break
        meanings_str = ''.join(meanings).strip()
        sentences_str = ''.join(sentences).strip()
        # for i in idiom_info:
        #     # на этом этапе необходимо распределить инфу в соответствии с тэгами
        #     # один тэг для значений, другой для примеров
        #     # не забыть ограничить количество оных до пяти включительно
        #     if "Origin" in i:
        #         break
        #     else:
        #         idiom_content_tmp.append(i)
        # print(meanings)
    #     for item in idiom_content_tmp:
    #         bar = str(item).replace("</li>", "\n")  # replace("<strong>", "**").replace("</strong>", "**")
    #         with_n_bar = re.sub("<[^>]*>", " ", unicodedata.normalize("NFKD", bar))
    #         idiom_content_without_tags.append(with_n_bar.strip())
        idiom_name = link.split(".com/")[-1].replace("/", "").replace("-", " ")
        # print(idiom_name)
        idiom_content[idiom_name] = {
            "idiom_name": idiom_name,
            "idiom_meaning": meanings_str,
            "idiom_examples": sentences_str
        }
        # print(idiom_content)

        with open("data/idiom_info.json", "w") as file:
            json.dump(idiom_content, file, indent=4, ensure_ascii=False)
    iteration_count -= 1
    print(f"Обход №{page_number} завершён, осталось обходов: {iteration_count}")
    if iteration_count == 0:
        print("Сбор данных завершен")