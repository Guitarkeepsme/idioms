from bs4 import BeautifulSoup
import unicodedata
import requests
import json
gimport re

all_links = []
all_links_set = set(all_links)
page_iteration_count = 151
print(f"Всего страниц: {page_iteration_count}")

for page_number in range(1, 152):
    url = "https://www.theidioms.com/list"
    r = requests.get(url + f"/page/{page_number}/")

    soup = BeautifulSoup(r.text, "lxml")
    links = []
    for idiom_url in soup.find_all('a'):
        if '-' not in idiom_url.get('href') or '#' in idiom_url.get('href'):
            pass
        else:
            links.append(idiom_url.get('href'))
    page_iteration_count -= 1
    print(f"Страница №{page_number} пройдена, осталось страниц: {page_iteration_count}")
    if page_iteration_count == 0:
        print("Все ссылки собраны!")

    all_links.extend(links)
    for link in all_links:
        all_links_set.add(link)

idiom_content = {}
info_iteration_count = 1519

for link in all_links_set:
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "lxml")
    idiom_info = soup.find("div", {"class": "article"})
    meanings_soup = idiom_info.find("ul")
    sentences_soup = idiom_info.find("ol")
    meanings = []
    sentences = []
    meanings_counter = 0
    sentences_counter = 0
    if meanings_soup is None or sentences_soup is None:
        pass
    else:
        for phrase in meanings_soup:
            bar = str(phrase).replace("</li>", "END_LINE")
            with_n_bar = re.sub("<[^>]*>", "", unicodedata.normalize("NFKD", bar))
            meanings.append(with_n_bar.strip().replace("  ", " ").replace(".", ""))
            meanings_counter += 1
            if meanings_counter == 5:
                break
        for example in sentences_soup:
            bar = str(example).replace("</li>", "END_LINE")
            # .replace("<strong>", "BOLD").replace("</strong>", "BOLD")
            with_n_bar = re.sub("<[^>]*>", "", unicodedata.normalize("NFKD", bar))
            sentences.append(with_n_bar.strip().replace("   ", " ").replace("  ", " "))
            sentences_counter += 1
            if sentences_counter == 5:
                break
        meanings_str = ''.join(meanings)
        sentences_str = ''.join(sentences)
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

    info_iteration_count -= 1
    print(f"Фразеологизм №{1519 - info_iteration_count} взят, осталось фразеологизмов: {info_iteration_count}")
    if info_iteration_count == 0:
        print("Все фразеологизмы собраны!")
