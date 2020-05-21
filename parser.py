import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://google.com/search?q='+input()
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125',
           'accept': '*/*'}
FILE = 'sites.csv'



def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='r')

    sites = []
    for item in items:
        sites.append({
            'title': item.find('h3').get_text(strip=True),
            'url': item.find('a').get('href')
        })
    return sites

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название','URL'])
        for item in items:
            writer.writerow([item['title'],item['url']])

def parse():
    html = get_html(URL)
    if html.status_code == 200:

        sites = get_content(html.text)
        save_file(sites, FILE)
    else:
        print('ERROR')


parse()
