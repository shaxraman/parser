# v1.2
# Уже может качать файл
# Не забыть ввести логин и пароль

import requests
from bs4 import BeautifulSoup
from log import login, password                         # Хранятся логины и пароли

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }
data = {'os_username': login,      # Логин
        'os_password': password,   # Пароль
        'login': 'Войти',
        'os_destination': '/index.action',
        }
urls = ['https://wiki.i-core.ru/pages/viewpage.action?pageId=10551321',
    'https://wiki.i-core.ru/pages/viewpage.action?pageId=2916492',
    'https://wiki.i-core.ru/pages/viewpage.action?pageId=4456476',
    ]


def get_html(url, session):
    return session.get(url).text                        # Возвращает html страницу

def get_pdf_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    link = soup.find('a', id='action-export-pdf-link', href=True).get('href')
    title = soup.find('h1', id='title-text').getText().split()
    #print(title)
    #  print('url for download pdf -', 'https://wiki.i-core.ru' + link)
    return ['https://wiki.i-core.ru' + link, title]     # Возвращает url для скачивания PDF файла

def download_file(url, title, session):
    r = session.get(url, stream=True)
    #print(r.headers)
    #print(r.url)

    with open(f'{title}.pdf', 'wb') as f:
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
    #input('ololo')
