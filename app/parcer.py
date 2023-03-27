import datetime
import os
import schedule
import requests
from bs4 import BeautifulSoup as bs

from app.accessor import add_data_sqlalchemy
from app.database import run_engine


def download_html(data_for_parcing):
    if not os.path.exists(data_for_parcing['dir_name']):
        os.makedirs(data_for_parcing['dir_name'])

    r = requests.get(data_for_parcing['url'])
    with open(data_for_parcing['url_to_main_file'], 'w', encoding='utf-8') as f:
        f.write(r.text)

    r = requests.get(data_for_parcing['url_tags'])
    with open(data_for_parcing['url_to_tags_file'], 'w', encoding='utf-8') as f:
        f.write(r.text)


def parcer_data(data_for_parcing):
    with open(data_for_parcing['url_to_main_file'], encoding='utf-8') as f:
        soup = bs(f, "lxml")
    stars = soup.find(id="repo-stars-counter-star")['title'].replace(',', '')
    fork = soup.find(id="repo-network-counter")['title'].replace(',', '')
    last_commit = soup.find('relative-time')['datetime']

    with open(data_for_parcing['url_to_tags_file'], encoding='utf-8') as f:
        soup = bs(f, "lxml")
    last_release = soup.find('relative-time')
    if last_release:
        last_release = last_release['datetime']

    return (stars, fork, last_commit, last_release)



def parce_urls(urls):
    for url in urls:
        dir_name = 'data_from_github/' + url[19:].replace('/', '_') + '/' + str(datetime.date.today())
        data_for_parcing = {'url': url,
                            'url_tags': url + '/tags',
                            'dir_name': dir_name,
                            'url_to_main_file': dir_name + '/main.html',
                            'url_to_tags_file': dir_name + '/tags.html'}

        download_html(data_for_parcing)
        parce_result = parcer_data(data_for_parcing)
        run_engine()
        add_data_sqlalchemy(url, *parce_result)


def repeat(days: int, at: str, urls: list):
    schedule.every(days).day.at(at).do(parce_urls(urls))
    while True:
        schedule.run_pending()
