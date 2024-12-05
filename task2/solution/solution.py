import csv
from collections import defaultdict
from pathlib import Path

import requests_cache
from bs4 import BeautifulSoup
from requests import RequestException
from tqdm import tqdm

from exceptions import ParserException

BASE_DIR = Path(__file__).parent
FILE_NAME = 'beasts.csv'
FILE_PATH = BASE_DIR / FILE_NAME
MAIN_URL = (
    'https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту'
)
WIKI_URL = 'https://ru.wikipedia.org/'
PARSER_ERROR = 'Ошибка в работе программы: {error}'
PARSER_STOP = 'Парсер завершил работу'
RESPONSE_ERROR = 'Возникла ошибка при загрузке страницы {url} {error}'


def file_output(results):
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        csv.writer(
            f,
            dialect=csv.unix_dialect
        ).writerows(
            results
        )


def get_response(session, url, encoding='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException as error:
        raise ConnectionError(
            RESPONSE_ERROR.format(url=url, error=error)
        )


def create_soup(session, url, features='lxml'):
    return BeautifulSoup(get_response(session, url).text, features=features)


def find_animals(session, url):
    animals_count = defaultdict(int)
    while True:
        for animal in tqdm(
            create_soup(session, url).select(
                'div.mw-category-columns ul li'
            )
        ):
            first_letter = animal.text[0]
            if first_letter.isascii() and first_letter.isalpha():
                continue
            else:
                animals_count[first_letter] += 1

        next_button = create_soup(session, url).select_one(
            '#mw-pages a:-soup-contains("Следующая страница")'
        )
        if next_button:
            url = WIKI_URL + next_button['href']
        else:
            break
    return animals_count.items()


def main():
    try:
        session = requests_cache.CachedSession()
        results = find_animals(session, MAIN_URL)
    except ParserException as error:
        raise error
    file_output(results)


if __name__ == '__main__':
    main()
