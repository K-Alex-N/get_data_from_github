import datetime
import json
import os
import requests

from flask import Blueprint, redirect, url_for, send_file
from flask import request
from flask import flash
from flask import render_template
from flask_login import current_user, login_required
from bs4 import BeautifulSoup as bs

from app.store.db.models_w_flsak_alchemy import PullRequest, Url, ParseData
from app.run_app import db
from app.store.parser.accessor import create_pull_request, get_urls_by_pull_request_id

parser = Blueprint('parser', __name__)


@parser.route('/')
def parcing_lists_page():
    pull_requests = PullRequest.query.all()
    url = Url.query.all()
    return render_template('app/parsing_lists.html', user=current_user, pull_requests=pull_requests, url=url)

def parse_urls(urls):
    for u in urls:
        # Parse data
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
        else:
            # не верный url
            stars, fork, last_commit, last_release = 'Error!', 'Error!', 'Error!', 'Error!'

        # save data in DB
        try:
            parse_data = ParseData(url_id=u.id,
                                   added_at=datetime.datetime.now(),
                                   stars=stars,
                                   fork=fork,
                                   last_commit=last_commit,
                                   last_release=last_release)
            db.session.add(parse_data)
            db.session.commit()
            # db.session.close()

        except Exception as e:
            print(e)
            return False
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
        # frequency = int(request.form['frequency'])

        error = check_data(name, links)
        if error:
            flash(error, category='error')
        else:
            pull_request_id = create_pull_request(name, links)
            if pull_request_id:
                # первый парсинг
                urls = get_urls_by_pull_request_id(pull_request_id)


                if parse_urls(urls):
                    flash('Парсер успешно добавлен. Рекомендуется проверить .json файл через 1-2 минуты.', category='success')
                    # дб пересылка на страницу пользователя, а точнее на страницу данного задания на парсинг в странице пользователя
                    # return redirect(url_for("parse_details", id=pull_request.id))
                    return redirect(url_for('parser.parcing_lists_page', user=current_user))
                flash('Ошибка запуска первого парсинга', category='error')
            else:
                flash('Обшибка добавления в БД', category='error')

    return render_template('app/add_new_parsing.html', user=current_user)


@parser.route('/download_json/<int:pull_request_id>/<path:file_name>', methods=['POST', 'GET'])
def download_json(pull_request_id, file_name):
    file_path = f"app/store/data/json/{pull_request_id}"
    if not os.path.isfile(file_path):
        # get data from DB. Put data in a dictionary
        d = {}
        # TODO ПЕРЕПИСАТЬ через db.session.execute(db.select(...).where...)!!!
        # TODO try_except function
        urls_id = Url.query.filter_by(pull_request_id=pull_request_id)
        for u in urls_id:
            d[u.id] = {}
            data_by_url_id = ParseData.query.filter_by(url_id=u.id)
            for data in data_by_url_id:
                d[u.id][data.added_at] = {
                    'stars': data.stars,
                    'fork': data.fork,
                    'last_commit': data.last_commit,
                    'last_release': data.last_release}

        # create JSON file
        with open(file_path, "w") as f:
            json.dump(d, f)

    # Sent file
    return send_file(f'store/data/json/{pull_request_id}',
                     as_attachment=True,
                     download_name=f'{file_name} {str(datetime.date.today())}.json'
                     )

@parser.route('/delete/<int:pull_request_id>', methods=['POST', 'GET'])
@login_required
def delete_parser(pull_request_id):
    pass


@parser.route('/how_to_use')
def how_to_use():
    return render_template('app/how_to_use.html', user=current_user)
