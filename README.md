Проект содержит 2 программы, которые парсят сайт myanimelist.

Программа Parser собирает с myanimelist список аниме-сериалов; каждый аниме-сериал имеет список параметров (название, рейтинг, год выпуска и т.д.), этот список тоже парсится.
Итогом работы программы является файл формата json. Файл содержит уже готовые данные (строки очищены от мусорной информации, некоторые строки переведены в числовой формат),
этими данными можно наполнить базу данных. Сейчас парсер имеет захардкоженное количество аниме, которое он может обработать. Этот недостаток будет исправлен в будущем.
Во второй версии программы у нее появилась возможность начинать парсинг с последнего айди, на котором он закончился, а не начинать парсинг заново. Последний айди хранится
в файле last_session.txt.

Программа linkparser собирает с myanimelist ссылки на аниме-сериалы. Эта программа так же имеет инструмент контроля сессий.
