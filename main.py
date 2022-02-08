import argparse
import os

from urllib.parse import urlparse

import requests

from dotenv import load_dotenv


def shorten_link(entered_link, BITLY_HEADERS):
    response = requests.post(
        url='https://api-ssl.bitly.com/v4/bitlinks',
        headers=BITLY_HEADERS,
        json={'long_url': entered_link}
    )
    response.raise_for_status()
    return response.json()["id"]
    

def count_click(parced_bitlink, BITLY_HEADERS):
    bitlink = f'{parced_bitlink.netloc}{parced_bitlink.path}'
    response = requests.get(
        url=f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
        headers=BITLY_HEADERS
    )
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(parsed_link, BITLY_HEADERS):
    link = f'{parsed_link.netloc}{parsed_link.path}'
    response = requests.get(
        url=f'https://api-ssl.bitly.com/v4/bitlinks/{link}',
        headers=BITLY_HEADERS
    )
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    
    token = os.getenv('BITLINK_TOKEN')

    bitly_headers = {'Authorization': f'Bearer {token}'}

    parser = argparse.ArgumentParser(description='Программа сокращает ссылки и показывает количество переходов по сокращенным ссылкам')
    parser.add_argument('link', help='https://www.google.com')
    args = parser.parse_args()
    link = args.link
    if is_bitlink(urlparse(link), bitly_headers):
        try:
            clicks = count_click(urlparse(link), bitly_headers)
            print(f'Количество переходов: {clicks}')
        except requests.exceptions.HTTPError as error:
            exit('Сервер не отвечает:\n{0}'.format(error))
    else:
        try:
            bitlink = shorten_link(link, bitly_headers)
            print(f'Битлинк: {bitlink}')
        except requests.exceptions.HTTPError as error:
            exit('ОШИБКА: Неверный формат ссылки, либо не отвечает сервер:\n{0}'.format(error))
