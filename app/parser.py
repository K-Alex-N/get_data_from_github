import datetime
import json
import os
import requests

from flask import Blueprint, redirect, url_for, send_file, send_from_directory
from flask import request
from flask import flash
from flask import render_template
from flask_login import current_user, login_required
from bs4 import BeautifulSoup as bs
from sqlalchemy import select

from app.store.db import session, try_except_session
from app.store.db.models import PullRequest, Url, ParseData
from app.store.parser.accessor import create_pull_request, create_dict_by_pull_request_id
from config.config import PATH_TO_JSON

parser = Blueprint('parser', __name__)


@parser.route('/')
def parcing_lists_page():
    pull_requests = session.scalars(select(PullRequest)).all()
    url = session.scalars(select(Url)).all()
    return render_template('app/parsing_lists.html', user=current_user, pull_requests=pull_requests, url=url)

def parse_urls(urls):
    for u in urls:
        r = requests.get(u.url)
        soup = bs(r.text, "lxml")
        stars = soup.find(id="repo-stars-counter-star")
        if stars: # если не найдены "stars" то значит не верный URL
            stars = stars['title'].replace(',', '')
            fork = soup.find(id="repo-network-counter")['title'].replace(',', '')
            last_commit = soup.find('relative-time')['datetime']

            r = requests.get(u.url + '/tags')
            soup = bs(r.text, "lxml")
            last_release = soup.find('relative-time')
            if last_release:
                last_release = last_release['datetime']
        else: # пока не верный url обозначаем так
            stars, fork, last_commit, last_release = 'Error!', 'Error!', 'Error!', 'Error!'

        parse_data = ParseData(url_id=u.id,
                               stars=stars,
                               fork=fork,
                               last_commit=last_commit,
                               last_release=last_release)

        with try_except_session() as session:
            session.add(parse_data)

    return True


def check_data(name, links: set):
    if not name:
        return 'Введите название'
    elif not links:
        return 'Введите ссылки на репозитории'
    else:
        for link in links:
            if 'github.com' not in link:
                return 'Введите полную ссылку на репозиторий (пример https://github.com/django/django)'


@parser.route('/add', methods=['POST', 'GET'])
@login_required
def add_new_parcing():
    if request.method == 'POST':
        name = request.form.get('name')
        links = set(request.form.get('links').split())

        error = check_data(name, links)
        if error:
            flash(error, category='error')
        else:
            pull_request_id = create_pull_request(name, links)
            if pull_request_id:
                # запуск первого парсинга
                urls = session.scalars(select(Url).where(Url.pull_request_id == pull_request_id)).all()
                if parse_urls(urls):
                    flash('Задание на парсинг успешно добавлено. Первый парсинг запущен. Рекомендуется проверить результат (.json файл или почту) через 1-2 минуты.', category='success')
                    # дб пересылка на страницу пользователя, а точнее на страницу данного задания на парсинг в странице пользователя
                    # return redirect(url_for("parse_details", id=pull_request.id))
                    return redirect(url_for('parser.parcing_lists_page', user=current_user))
                flash('Ошибка запуска первого парсинга', category='error')
            else:
                flash('Обшибка добавления в БД', category='error')

    return render_template('app/add_new_parsing.html', user=current_user)


@parser.route('/download_json/<int:pull_request_id>/<path:file_name>', methods=['POST', 'GET'])
def download_json(pull_request_id, file_name):
    file_path = os.path.join(PATH_TO_JSON, str(pull_request_id))
    if not os.path.isfile(file_path):
        d = create_dict_by_pull_request_id(pull_request_id)
        with open(file_path, "w") as f:
            json.dump(d, f)

    return send_from_directory(PATH_TO_JSON, str(pull_request_id),
                               as_attachment=True,
                               download_name=f'{file_name} {str(datetime.date.today())}.json'
                               )

@parser.route('/delete/<int:pull_request_id>', methods=['POST', 'GET'])
@login_required
def delete_parser(pull_request_id):
    with try_except_session() as session:
        pull_request = session.scalar(select(PullRequest).where(PullRequest.id == pull_request_id))
        session.delete(pull_request)
    return parcing_lists_page()

@parser.route('/how_to_use')
def how_to_use():
    return render_template('app/how_to_use.html', user=current_user)
