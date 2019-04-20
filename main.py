# v1.1
# Выдае url для скачивания файла
# Не забыть ввести логин и пароль

import requests
from bs4 import BeautifulSoup
from log import login, password                 # Хранятся логины и пароли

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }
data = {'os_username': login,      # Логин
        'os_password': password,   # Пароль
        'login': 'Войти',
        'os_destination': '/index.action',
        }
url = 'https://wiki.i-core.ru/pages/viewpage.action?pageId=10551321'


def loggin_to_site(url):
    s = requests.Session()                      # Для сохранения сессии
    s.post(url, headers=headers, data=data)     # Лонинемся на сайт
    #print(a.headers)
    return s.get(url).text                      # Возвращает html страницу


def get_pdf_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    link = soup.find('a', id='action-export-pdf-link', href=True).get('href')
    # print('url for download pdf -', 'https://wiki.i-core.ru' + link)
    return 'https://wiki.i-core.ru' + link      # Возвращает url для скачивания PDF файла

def download_file(url):
    s = requests.Session()                      # Для сохранения сессии
    s.post(url, headers=headers, data=data)
    r = s.get(url, stream=True)

    print(r.headers)
    print(r.url)

    with open('1.pdf', 'wb') as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)

if __name__ == '__main__':
    logging = loggin_to_site(url)
    link = get_pdf_link(logging)

    download_file(link)
