# v1.3
# author Nezamov S.

import requests
from bs4 import BeautifulSoup
import datetime
import os
import getpass

def login():
    userName = input('Напишите Ваш логин ')
    password = getpass.getpass()
    if '@' in userName:
        return userName[:userName.index('@')], password
    elif '.i' in userName:
        return userName[:userName.index('.i')], password
    else:
        return userName, password
log = login()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }
data = {'os_username': log[0],      # Логин
        'os_password': log[1],   # Пароль
        'login': 'Войти',
        'os_destination': '/index.action',
        }
urls = []

now = datetime.datetime.now()
new_directory = f'wiki {now.day}-{now.month}-{now.year}'    # Создаем папку wiki + текущая дата
def create_dir():
    try:
        os.mkdir(f'./{new_directory}')
    except:
        pass

def read_urls(name_file):
    with open(name_file) as f:
        for i in f:
            if 'wiki' in i:
                urls.append(i.strip())   # Собираем список url из сайта

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

    create_dir()
    read_urls('urls.txt')
    with requests.Session() as s:                                           # Для сохранения сессии
        s.post('https://wiki.i-core.ru', headers=headers, data=data)        # Логинемся на сайт
        for url in urls:
            try:
                html = get_html(url, s)
                try:
                    link = get_pdf_link(html)
                    download_file(link[0], link[1], s)
                except:
                    pass
            except:
                pass


if __name__ == '__main__':
    main()
    print('ready')
