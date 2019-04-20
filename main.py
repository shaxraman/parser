# v1.2
# Выдае url для скачивания файла
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
url = 'https://wiki.i-core.ru/pages/viewpage.action?pageId=10551321'


def get_html(url, session):
    return session.get(url).text                    # Возвращает html страницу

def get_pdf_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    link = soup.find('a', id='action-export-pdf-link', href=True).get('href')
    #  print('url for download pdf -', 'https://wiki.i-core.ru' + link)
    return 'https://wiki.i-core.ru' + link              # Возвращает url для скачивания PDF файла

def download_file(url, session):
    r = session.get(url, stream=True)
    print(r.headers)
    print(r.url)

    with open('1.pdf', 'wb') as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)

def main():
    with requests.Session() as s:                                           # Для сохранения сессии
        s.post('https://wiki.i-core.ru', headers=headers, data=data)        # Логинемся на сайт
        link = get_pdf_link(get_html(url, s))
        download_file(link, s)



if __name__ == '__main__':
    main()
