from Decorators2 import logger
from functools import wraps
import os

@logger(path='data2.log')
def scraping(number_of_pages):
    import re
    import requests
    import bs4

    url_base = 'https://habr.com'
    url_ru = 'https://habr.com/ru/all/'
    url_page = '/ru/all/page'
    HEADERS = {
        'Cookie': '_ym_uid=1639148487334283574; _ym_d=1639149414; _ga=GA1.2.528119004.1639149415; _gid=GA1.2.512914915.1639149415; habr_web_home=ARTICLES_LIST_ALL; hl=ru; fl=ru; _ym_isad=2; __gads=ID=87f529752d2e0de1-221b467103cd00b7:T=1639149409:S=ALNI_MYKvHcaV4SWfZmCb3_wXDx2olu6kw',
        'Accept-Language': 'ru-RU,ru;q=0.9',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'If-None-Match': 'W/"37433-+qZyNZhUgblOQJvD5vdmtE4BN6w"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
        'sec-ch-ua-mobile': '?0'
        }
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']


    arts_previews = []
    preview = []
    links = []
    for page in range(number_of_pages):
        url = f'{url_base}{url_page}{page}/'
        data_page = requests.get(url, headers=HEADERS)
        text_page = data_page.text
        soup_page = bs4.BeautifulSoup(text_page, features='html.parser')
        articles_soup = soup_page.find_all('article')
        for article in articles_soup:
            preview_soup = article.find_all(
                class_ ="article-formatted-body article-formatted-body article-formatted-body_version-2")
            for position in preview_soup:
                preview = position.text
                links.append(f"{url_base}{article.find(class_='tm-article-snippet__title-link').attrs['href']}")
                for tag in KEYWORDS:
                    if re.search(tag, preview):
                        date = article.find(class_="tm-article-snippet__datetime-published").text
                        title = article.find(class_="tm-article-snippet__title tm-article-snippet__title_h2").text
                        link = f"{url_base}{article.find(class_='tm-article-snippet__title-link').attrs['href']}"
                        result = f'{date} - {title} - {link}'
                        arts_previews.append(result)
                        break
    print(f'Количество статей с совпадением в превью: {len(arts_previews)}')
    print(arts_previews, '\n')

    arts_articles = []
    for position in links:
        data_article = requests.get(position, headers=HEADERS).text
        soup_article = bs4.BeautifulSoup(data_article, features='html.parser')
        text_article = soup_article.find_all(class_="article-formatted-body article-formatted-body article-formatted-body_version-2")
        for blocks in text_article:
            block = blocks.text
            for tag in KEYWORDS:
                if re.search(tag, block):
                    date = soup_article.find(class_="tm-article-snippet__datetime-published").text
                    title = soup_article.find(class_="tm-article-snippet__title tm-article-snippet__title_h1").text
                    link = position
                    result = f'{date} - {title} - {link}'
                    arts_articles.append(result)
                    break
    body = f'Количество статей с совпадением в текстах: {len(arts_articles)}'
    print(body)
    print(arts_articles)
    return body


if __name__ == "__main__":
    number_of_pages = 3
    scraping(number_of_pages)
