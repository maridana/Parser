"""Эта программа парсит сайт myanimelist.

Она собирает с него список аниме-сериалов; каждый аниме-сериал имеет список параметров (название, рейтинг, год выпуска и т.д.), этот список тоже парсится.
Итогом работы программы является файл формата json. Файл содержит уже готовые данные (строки очищены от мусорной информации, некоторые строки переведены в числовой формат),
этими данными можно наполнить базу данных. Сейчас парсер имеет захардкоженное количество аниме, которое он может обработать. Этот недостаток будет исправлен в будущем.

Во второй версии программы у нее появилась возможность начинать парсинг с последнего айди, на котором он закончился, а не начинать парсинг заново. Последний айди хранится
в файле last_session.txt.
"""

import json
import re
import requests
import time

from bs4 import BeautifulSoup as BS

try:
    with open('data.json', 'r') as file_list:
        anime_list = json.load(file_list)
except:
    anime_list = []

try:
    file = open('last_session.txt', 'r')
    session = int(file.readline())
    file.close()
except:
    session = 0

page = session + 1

while page <= 10: # Число страниц - число анимешек, которое обрабатывает программа. Место с хардкодом.

    r = requests.get('https://myanimelist.net/anime/' + str(page))
    html = BS(r.content, 'html.parser')

    not_found = '' # Строка, хранящая то, страница 404 у нас или нет.

    for not_found in html.find_all('div', {'class': 'error404'}):
        not_found1 = not_found.text

    for title in html.find_all('h1', {'class': 'title-name h1_bold_none'}):
        title1 = str(page) + ' ' + title.text

    for desc in html.select(".rightside"):
        desc1 = desc.find('p')

    for year in html.find_all('span', {'class': 'dark_text'}, string='Aired:'):
        year1 = year.find_parent("div", "spaceit_pad") # Здесь ищется нужный кусок страницы. Все дальнейшие операции - чистка данных и приведение строки к int.
        year2 = year1.find("span", {"class": "dark_text"})
        year2.decompose()
        year3 = year1.text
        year3 = year3.strip("\n ")
        year4 = re.search(r'\d{4}', year3)
        year5 = int(year4.group(0))

    for genre in html.find_all("span",
                               {"class": "dark_text"}, string="Genres:"):
        list1 = [] # Список жанров объявляется здесь, чтобы у каждой анимешки был свой список жанров, они не дублировались и не терялись.
        genre1 = genre.find_parent("div", "spaceit_pad") # Поиск нужного куска страницы, далее следует чистка данных от лишнего. 
        genre2 = genre1.find("span", {"class": "dark_text"})
        genre2.decompose()
        for genre3 in genre1.find_all('a'):
            genre3.decompose()
        for genre5 in genre1.find_all("span", {"style": "display: none"}):
            genre6 = genre5.text
            list1.append(genre6) # Составление списка жанров.

    for score in html.find_all("div", {"class": "score-label"},
                               {"itemprop": "ratingValue"}):
        score1 = score.text

    for image in html.find_all("div", {"style": "text-align: center;"}):
        image1 = image.select_one('img').get('data-src')

    if not_found == "": # Проверка, страница 404 или нет. Если нет, то не добавляем ничего в список, чтобы не было дубликатов.
        anime_list.append({'title': title.text,
                           'synopsis': desc1.text,
                           'year': year5,
                           'genres': list1,
                           'rating': float(score1),
                           'image': image1,
                           'myAnimeListLink':
                           'https://myanimelist.net/anime/' + str(page)})
    
    file = open('last_session.txt', 'w')
    file.write(str(page))
    file.close()

    file = open('last_session.txt', 'r')
    session = int(file.readline())
    file.close()

    time.sleep(3) # Перерыв работы парсера, чтобы не вызвать включение дудос-защиты сайта.
    page += 1

    with open('data.json', 'w') as file_list:
        json.dump(anime_list, file_list, indent=4)
