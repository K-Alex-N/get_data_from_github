import os
import schedule
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

from model import add_data_row_sql, add_data_sqlalchemy, run_engine, get_data_sqlalchemy


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
    dir_name = url[8:].replace('/', '_')
    file_main = dir_name + '/main.html'
    file_tags = dir_name + '/tags.html'
    url_tags = url + '/tags'
    if get_html:
        download_html(url, dir_name, file_main, file_tags, url_tags)

    with open(file_main, encoding='utf-8') as f:
        soup = bs(f, "lxml")
    stars = soup.find(id="repo-stars-counter-star")['title'].replace(',', '')
    fork = soup.find(id="repo-network-counter")
    if fork:
        fork = fork['title'].replace(',', '')

    last_commit = soup.find('relative-time')
    if last_commit:
        last_commit = last_commit['datetime']

    with open(file_tags, encoding='utf-8') as f:
        soup = bs(f, "lxml")
    last_release = soup.find('relative-time')
    if last_release:
        last_release = last_release['datetime']

    print(stars)
    print(fork)
    print(last_commit)
    print(last_release)

    if save_data:
        add_data_sqlalchemy(url, stars, fork, last_commit, last_release)
        # add_data_row_sql(url, stars, fork, last_commit, last_release)
        # вероятно нужно подключить sqlalchemy для ORM запросов


def parce_urls(urls):
    for url in urls:
        parcer(url, get_html, save_data)


def repeat(days: int, at: str):
    schedule.every(days).day.at(at).do(parce_urls)
    while True:
        schedule.run_pending()


if __name__ == '__main__':

    # get_html = False  # True -> если нужно скачать новый html
    # save_data = True
    # urls = [
    #     'https://github.com/django/django',
    #     'https://github.com/mingrammer/python-web-framework-stars'
    # ]
    #
    # is_repeat_active = False  # True -> если нужно включить повтор по времени
    # if is_repeat_active:
    #     days = 1
    #     at = '8:50'
    #     repeat(days, at)
    # else:
    #     parce_urls(urls)

    get_data_sqlalchemy()
