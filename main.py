# v1.0
# Выдае url для скачивания файла
# Не забыть ввести логин и пароль

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }
data = {'os_username': 'login',
        'os_password': 'password',
        'login': 'Войти',
        'os_destination': '/index.action',
        }
url = 'https://wiki.i-core.ru/pages/viewpage.action?pageId=10551321'

s = requests.Session()
s.post(url, headers=headers, data=data)
a = s.get(url).text
#print(a.encode("utf-8"))  # Показать HTML страницы


soup = BeautifulSoup(a, 'html.parser')
link = soup.find('a', id='action-export-pdf-link', href=True).get('href')

print('new_url -', 'https://wiki.i-core.ru' + link)
