import requests
from bs4 import BeautifulSoup

for page_number in range(13, 15):
    url = "https://www.theidioms.com/list/"
    r = requests.get(url + f"page/{page_number}/")
    soup = BeautifulSoup(r.text, "html.parser")
    idiom_url = soup.find('div', class_='new-list').find('a')
    print(idiom_url)