import os
import argparse

from urllib.parse import urlparse
from dotenv import load_dotenv

import requests

TOKEN = os.getenv('BITLINK_TOKEN')

BITLY_HEADERS = {'Authorization': f'Bearer {TOKEN}'}


def shorten_link(entered_link):
    response = requests.post(
        url='https://api-ssl.bitly.com/v4/bitlinks',
        headers=BITLY_HEADERS,
        json={'long_url': entered_link}
    )
    response.raise_for_status()
    return response.json()["id"]
    

def count_click(parced_bitlink):
    bitlink = f'{parced_bitlink.netloc}{parced_bitlink.path}'
    response = requests.get(
        url=f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
        headers=BITLY_HEADERS
    )
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(parsed_link):
    link = f'{parsed_link.netloc}{parsed_link.path}'
    response = requests.get(
        url=f'https://api-ssl.bitly.com/v4/bitlinks/{link}',
        headers=BITLY_HEADERS
    )
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser(description='Программа сокращает ссылки и показывает количество переходов по сокращенным ссылкам')
    parser.add_argument('link', help='https://www.google.com')
    args = parser.parse_args()
    link = args.link
    if is_bitlink(urlparse(link)):
        try:
            clicks = count_click(urlparse(link))
            print(f'Количество переходов: {clicks}')
        except requests.exceptions.HTTPError as error:
            exit('Сервер не отвечает:\n{0}'.format(error))
    else:
        try:
            bitlink = shorten_link(link)
            print(f'Битлинк: {bitlink}')
        except requests.exceptions.HTTPError as error:
            exit('ОШИБКА: Неверный формат ссылки, либо не отвечает сервер:\n{0}'.format(error))
