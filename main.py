# v1.2
# Уже может качать файл
# Не забыть ввести логин и пароль

import requests
from bs4 import BeautifulSoup
from log import login, password                         # Хранятся логины и пароли
import datetime
import os

try:
    now = datetime.datetime.now()
    new_directory = f'wiki {now.day}-{now.month}-{now.year}'    # Создаем папку wiki + текущая дата
    os.mkdir(f'./{new_directory}')
except:
    pass

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }
data = {'os_username': login,      # Логин
        'os_password': password,   # Пароль
        'login': 'Войти',
        'os_destination': '/index.action',
        }
urls = []
with open('url.txt') as f:
    for i in f:
        if 'wiki' in i:
            urls.append(i.strip())

def get_html(url, session):
    return session.get(url).text                        # Возвращает html страницу

def get_pdf_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    link = soup.find('a', id='action-export-pdf-link', href=True).get('href')
    title = soup.find('h1', id='title-text').text
    return ['https://wiki.i-core.ru' + link, title.split()]     # Возвращает url для скачивания PDF файла

def download_file(url, title, session):
    r = session.get(url, stream=True)

    with open(f'{new_directory}/{" ".join(title)}.pdf', 'wb') as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)

def main():
    with requests.Session() as s:                                           # Для сохранения сессии
        s.post('https://wiki.i-core.ru', headers=headers, data=data)        # Логинемся на сайт
        for url in urls:
            html = get_html(url, s)
            link = get_pdf_link(html)
            download_file(link[0], link[1], s)


if __name__ == '__main__':
    main()
