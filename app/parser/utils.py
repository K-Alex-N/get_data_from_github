import json
import os
import requests

from flask import flash, abort
from flask_login import current_user
from bs4 import BeautifulSoup as bs
from sqlalchemy import select

from app.store.db import session, try_except_session
from app.store.db.models import PullRequest, Url, ParseData
from config.config import PATH_TO_JSON


# ---------------------------------------------------------------- #
# pull request management
# ---------------------------------------------------------------- #

def add_or_change(request, type, pull_request_id: int = 0):
    name = request.form.get('name')
    set_links = set(request.form.get('links').split())

    error = check_data(name, set_links)
    if error:
        flash(error, category='error')
    else:
        if type == 'add':
            pull_request_id = create_new_parser(name, set_links)
        elif type == 'change':
            pull_request_id = change_parser(name, set_links, pull_request_id)

        if pull_request_id:
            run_first_parsing(pull_request_id, type)


def check_data(name, links: set):
    if not name:
        return 'Введите название'
    elif not links:
        return 'Введите ссылки на репозитории'
    else:
        for link in links:
            if 'github.com' not in link:
                return 'Введите полную ссылку на репозиторий (пример https://github.com/django/django)'


def create_new_parser(name, links):
    pull_request = PullRequest(name=name, user_id=current_user.id)
    with try_except_session() as session:
        session.add(pull_request)
        session.flush()

        for link in links:
            url = Url(pull_request_id=pull_request.id, url=link)
            session.add(url)

    return pull_request.id


def change_parser(name, new_links_str: set[str], pull_request_id: int):
    with try_except_session() as session:
        pull_request = session.scalar(select(PullRequest).where(PullRequest.id == pull_request_id))
        # change name
        if pull_request.name != name:
            pull_request.name = name
        # change links
        cur_links_odj = session.scalars(select(Url).where(Url.pull_request_id == pull_request.id)).all()
        # все старое (то что не повторилось в new_links) удаляем
        for link in cur_links_odj:
            if link.url in new_links_str:
                new_links_str.remove(link.url)
            else:
                session.delete(link)
        # все оставщееся из new_links добавляем
        for link in new_links_str:
            session.add(
                Url(
                    pull_request_id=pull_request_id,
                    url=link)
            )

    return pull_request_id


def is_exist(pull_request_id: int):
    ids = session.scalars(select(PullRequest.id)).all()
    if pull_request_id not in ids:
        abort(404)


# ---------------------------------------------------------------- #
# parsing
# ---------------------------------------------------------------- #
def run_first_parsing(pull_request_id, type):
    urls = session.scalars(select(Url).where(Url.pull_request_id == pull_request_id)).all()
    if parse_urls(urls):
        flash(f'Задание на парсинг успешно {"добавлено" if type == "add" else "изменено"}. '
              f'Пробный парсинг запущен. '
              f'Рекомендуется проверить результат (.json файл).',
              category='success')
        return True
    flash('Ошибка запуска первого парсинга', category='error')


def parse_urls(urls):
    for u in urls:
        r = requests.get(u.url)
        soup = bs(r.text, "lxml")
        stars = soup.find(id="repo-stars-counter-star")
        if stars:  # если не найдены "stars" то значит не верный URL
            stars = stars['title'].replace(',', '')
            fork = soup.find(id="repo-network-counter")['title'].replace(',', '')
            last_commit = soup.find('relative-time')['datetime']

            r = requests.get(u.url + '/tags')
            soup = bs(r.text, "lxml")
            last_release = soup.find('relative-time')
            if last_release:
                last_release = last_release['datetime']
        else:  # пока не верный url обозначаем так
            stars, fork, last_commit, last_release = 'Error!', 'Error!', 'Error!', 'Error!'

        parse_data = ParseData(url_id=u.id,
                               stars=stars,
                               fork=fork,
                               last_commit=last_commit,
                               last_release=last_release)

        with try_except_session() as session:
            session.add(parse_data)

    return True


# ---------------------------------------------------------------- #
# json
# ---------------------------------------------------------------- #

def create_json(pull_request_id, file_path):
    d = create_dict_by_pull_request_id(pull_request_id)
    with open(file_path, "w") as f:
        json.dump(d, f)
def create_dict_by_pull_request_id(pull_request_id):
    d = {}
    urls_id = session.scalars(select(Url).where(Url.pull_request_id == pull_request_id)).all()
    for u in urls_id:
        d[u.url] = {}
        data_by_url_id = session.scalars(select(ParseData).where(ParseData.url_id == u.id)).all()
        for data in data_by_url_id:
            d[u.url][str(data.added_at.date())] = {
                'stars': data.stars,
                'fork': data.fork,
                'last_commit': data.last_commit,
                'last_release': data.last_release}
    return d


def delete_old_json_file(pull_request_id):
    path = f'{PATH_TO_JSON}/{pull_request_id}'
    if os.path.exists(path):
        os.remove(path)
