"""Эта программа парсит сайт myanimelist.

Она собирает с него ссылки на аниме-сериалы. Это первая версия программы, она пока не имеет инструмента контроля сессий.
"""

import json
import requests
import time

from bs4 import BeautifulSoup as BS

limit = 0

number = 0

link_list = []

while limit <= 50:

    r = requests.get('https://myanimelist.net/topanime.php?limit=' + str(limit))
    html = BS(r.content, 'html.parser')

    for link in html.find_all('h3', {'class': 'fl-l fs14 fw-b anime_ranking_h3'}):
        #print(number)
        link1 = link.select_one('a').get('href')
        number += 1
        #print(link1)
        link_list.append({ number : link1 })
    

    time.sleep(3)
    limit += 50

    with open('links.json', 'w') as file_list:
        json.dump(link_list, file_list, indent=4)