"""Эта программа парсит сайт myanimelist.

Она собирает с него ссылки на аниме-сериалы и имеет инструмента контроля сессий.
"""

import json
import requests
import time

from bs4 import BeautifulSoup as BS

try:
    with open('links.json', 'r') as file_list:
        link_dict = json.load(file_list)
except:
    link_dict = {}

try:
    file = open('last_linksession.txt', 'r')
    session = int(file.readline())
    file.close()
except:
    session = 0

try:
    file = open('last_limit.txt', 'r')
    session_limit = int(file.readline())
    file.close()
except:
    session_limit = 0

number = session

limit = session_limit

while limit <= 50:

    r = requests.get('https://myanimelist.net/topanime.php?limit=' + str(limit))
    html = BS(r.content, 'html.parser')

    for link in html.find_all('h3', {'class': 'fl-l fs14 fw-b anime_ranking_h3'}):
        #print(number)
        link1 = link.select_one('a').get('href')
        #print(link1)
        link_dict.update({ number : link1 })

        number += 1

        file = open('last_linksession.txt', 'w')
        file.write(str(number))
        file.close()

        file = open('last_linksession.txt', 'r')
        session = int(file.readline())
        file.close()
    
    limit += 50

    file = open('last_limit.txt', 'w')
    file.write(str(limit))
    file.close()

    file = open('last_limit.txt', 'r')
    session_limit = int(file.readline())
    file.close()

    time.sleep(3)

    with open('links.json', 'w') as file_list:
        json.dump(link_dict, file_list, indent=4)