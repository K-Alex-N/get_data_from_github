import datetime
import os
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup as bs

from app.parser import add_data_sqlalchemy
from app.parser import run_engine


def download_html(data_for_parcing: 'DataForParcing'):
    if not os.path.exists(data_for_parcing.dir_name):
        os.makedirs(data_for_parcing.dir_name)


    r = requests.get(data_for_parcing.url)
    with open(data_for_parcing.url_to_main_file, 'w', encoding='utf-8') as f:
        f.write(r.text)

    r = requests.get(data_for_parcing.url_tags)
    with open(data_for_parcing.url_to_tags_file, 'w', encoding='utf-8') as f:
        f.write(r.text)


def parcer_data(data_for_parcing: 'DataForParcing'):
    with open(data_for_parcing.url_to_main_file, encoding='utf-8') as f:
        soup = bs(f, "lxml")
        stars = soup.find(id="repo-stars-counter-star")['title'].replace(',', '')
        fork = soup.find(id="repo-network-counter")['title'].replace(',', '')
        last_commit = soup.find('relative-time')['datetime']

    with open(data_for_parcing.url_to_tags_file, encoding='utf-8') as f:
        soup = bs(f, "lxml")
        last_release = soup.find('relative-time')
        if last_release:
            last_release = last_release['datetime']

    return stars, fork, last_commit, last_release


@dataclass
class DataForParcing():
    url: str
    url_tags: str = None
    dir_name: str = None
    url_to_main_file: str = None
    url_to_tags_file: str = None

    def __post_init__(self):
        self.dir_name = 'data_from_github/' + self.url[19:].replace('/', '_') + '/' + str(datetime.date.today())
        self.url_tags = self.url + '/tags'
        self.url_to_main_file = self.dir_name + '/main.html'
        self.url_to_tags_file = self.dir_name + '/tags.html'


def parce_urls(urls):
    for url in urls:
        data_for_parcing = DataForParcing(url)

        download_html(data_for_parcing)
        parce_result = parcer_data(data_for_parcing)
        run_engine()
        add_data_sqlalchemy(url, *parce_result)
        print('end!')

