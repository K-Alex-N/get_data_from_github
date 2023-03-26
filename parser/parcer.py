import datetime
import os
import schedule
import requests
from bs4 import BeautifulSoup as bs

from parser.database import add_data_sqlalchemy


def download_html(url, dir_name, file_main, file_tags, url_tags):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    r = requests.get(url)
    with open(file_main, 'w', encoding='utf-8') as f:
        f.write(r.text)

    r = requests.get(url_tags)
    with open(file_tags, 'w', encoding='utf-8') as f:
        f.write(r.text)


def parcer(url, get_html, save_data):
    dir_name = 'data_from_github/' + url[19:].replace('/', '_') + '/' + str(datetime.date.today())
    file_main = dir_name + '/main.html'
    file_tags = dir_name + '/tags.html'
    url_tags = url + '/tags'

    if get_html:
        download_html(url, dir_name, file_main, file_tags, url_tags)

    with open(file_main, encoding='utf-8') as f:
        soup = bs(f, "lxml")
    stars = soup.find(id="repo-stars-counter-star")['title'].replace(',', '')
    fork = soup.find(id="repo-network-counter")['title'].replace(',', '')
    last_commit = soup.find('relative-time')['datetime']

    with open(file_tags, encoding='utf-8') as f:
        soup = bs(f, "lxml")
    last_release = soup.find('relative-time')
    if last_release:
        last_release = last_release['datetime']

    if save_data:
        add_data_sqlalchemy(url, stars, fork, last_commit, last_release)
        # add_data_row_sql(url, stars, fork, last_commit, last_release)


def parce_urls(urls, get_html=True, save_data=True):
    for url in urls:
        parcer(url, get_html, save_data)


def repeat(days: int, at: str, urls: list):
    schedule.every(days).day.at(at).do(parce_urls(urls))
    while True:
        schedule.run_pending()