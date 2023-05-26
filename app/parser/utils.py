import json
import os
import requests

from flask import flash, abort
from flask_login import current_user
from bs4 import BeautifulSoup as bs
from sqlalchemy import select

from app.db import session, try_except_session
from app.db import PullRequest, Url, ParseData
from config.config import JSON_DIR


# ---------------------------------------------------------------- #
# home page
# ---------------------------------------------------------------- #

def get_home_data():
    pull_requests = session.scalars(select(PullRequest)).all()
    url = session.scalars(select(Url)).all()
    data = []
    for pr in pull_requests:
        data.append([pr, [u for u in url if u.pull_request_id == pr.id]])

    return data


def add_pull_request(request):
    name = request.form.get('name')
    set_links = set(request.form.get('links').split())

    if check_data(name, set_links):
        pull_request_id = create_new_parser(name, set_links)
        if pull_request_id:
            run_first_parsing(pull_request_id, msg='добавлено')


def change_pull_request(request, pull_request_id):
    name = request.form.get('name')
    set_links = set(request.form.get('links').split())

    if check_data(name, set_links):
        if change_parser(name, set_links, pull_request_id):
            run_first_parsing(pull_request_id, msg='изменено')


def check_data(name, set_links):
    if not name:
        flash('Введите название', category='error')
        return False

    if not set_links:
        flash('Введите ссылки на репозитории', category='error')
        return False

    for link in set_links:
        if 'github.com' not in link:
            flash('Введите полную ссылку на репозиторий (пример https://github.com/django/django)', category='error')
            return False

    return True


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
            session.add(Url(pull_request_id=pull_request_id, url=link))

    return True


def is_exist(pull_request_id: int):
    ids = set(session.scalars(select(PullRequest.id)).all())
    if pull_request_id not in ids:
        abort(404)


def is_user_valid(user_id: int):
    if user_id != current_user.id:
        abort(403)


# ---------------------------------------------------------------- #
# parsing
# ---------------------------------------------------------------- #
def run_first_parsing(pull_request_id, msg):
    urls = session.scalars(select(Url).where(Url.pull_request_id == pull_request_id)).all()
    if parse_urls(urls):
        flash(f'Задание на парсинг успешно {msg}. '
              f'Пробный парсинг сделан. '
              f'Результат можно проверить в json-файле.',
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
            last_commit = soup.find('relative-time')
            if last_commit:
                last_commit = last_commit['datetime']

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


def delete_old_json_files(pull_request_id):
    path = os.path.join(JSON_DIR, str(pull_request_id))
    if os.path.exists(path):
        os.remove(path)
