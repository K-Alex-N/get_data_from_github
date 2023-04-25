import datetime
import json

import requests
from flask import Blueprint, redirect, url_for
from flask import request
from flask import flash
from flask import render_template
from flask_login import current_user, login_required
from bs4 import BeautifulSoup as bs

from app.models import PullRequest, Url, ParseData
from app.run_app import db

parser = Blueprint('parser', __name__)


@parser.route('/')
# @login_required - нельзя. любой приходящий должен увидеть список
def parcing_lists_page():
    pull_requests = PullRequest.query.all()
    url = Url.query.all()
    return render_template('app/parsing_lists.html', user=current_user, pull_requests=pull_requests, url=url)


# @parser.route('/<int:parcing_id>')
# def parcing_data_page(parcing_id):
#     return render_template('parsing_lists.html')

def parse_urls(urls):
    for u in urls:
        try:
            # Parse data
            r = requests.get(u.url)
            if '404 ' not in r.text:
                soup = bs(r.text, "lxml")
                stars = soup.find(id="repo-stars-counter-star")['title'].replace(',', '')
                fork = soup.find(id="repo-network-counter")['title'].replace(',', '')
                last_commit = soup.find('relative-time')['datetime']

                r = requests.get(u.url + '/tags')
                soup = bs(r.text, "lxml")
                last_release = soup.find('relative-time')
                if last_release:
                    last_release = last_release['datetime']
            else:
                # не верный url
                # пока так
                stars, fork, last_commit, last_release = 'Error!', 'Error!', 'Error!', 'Error!'

            # save data in DB
            parse_data = ParseData(url_id=u.id,
                                   added_at=datetime.datetime.now(),
                                   stars=stars,
                                   fork=fork,
                                   last_commit=last_commit,
                                   last_release=last_release)
            db.session.add(parse_data)
            db.session.commit()

        except Exception as e:
            print(e)
            return False
    return True

def check_data(name, links):
    if not name:
        return 'Введите название'
    elif not links:
        return 'Введите ссылки на репозитории'
    else:
        for link in links.split():
            if 'github.com' not in link:
                return 'Введите полную ссылку на репозиторий (пример https://github.com/django/django)'

@parser.route('/add', methods=['POST', 'GET'])
@login_required
def add_new_parcing():
    if request.method == 'POST':
        name = request.form.get('name')
        links = request.form.get('links')
        frequency = int(request.form['frequency'])

        error = check_data(name, links)
        if error:
            flash(error, category='error')
        else:
            try:
                # запись данных в БД
                pull_request = PullRequest(
                    name=name,
                    user_id=current_user.id,
                    start_date=datetime.datetime.now(),  # вот это можно перенести прямо в класс!!!
                    frequency=frequency,
                )
                db.session.add(pull_request)
                db.session.flush()

                for link in links.split():
                    url = Url(
                        pull_request_id=pull_request.id,
                        url=link
                    )
                    db.session.add(url)
                db.session.commit()

                # первый парсинг
                urls = Url.query.filter_by(pull_request_id=pull_request.id).all()
                if parse_urls(urls):
                    # дб пересылка на страницу пользователя, а точнее на страницу данного задания на парсинг в странице пользователя
                    # return redirect(url_for("parse_details", id=pull_request.id))
                    return redirect(url_for('parser.parcing_lists_page', user=current_user))
                flash('Ошибка запуска парсера', category='error')

            except:
                db.session.rollback()
                flash('Обшибка добавления в БД', category='error')


    return render_template('app/add_new_parsing.html', user=current_user)

@parser.route('/json', methods=['POST', 'GET'])
def create_JSON():
    """
    название файла это pull_request.id

    data = {
        url: {
            date: {
                parse_data
            },
            next_date: {},
        next_url: {}
        }

    data = {
        "https://github.com/django/django": {
            "2023-04-25 11:10:01.535551": {
                'stars': 70048,
                'fork': 29103,
                'last_commit': "2023-04-25T07:30:52Z",
                'last_release': "2023-04-05T05:53:22Z"
            }
        }
    """

    # get data from DB
    d = {}
    urls_id = Url.query.filter_by(pull_request_id=11)
    for u in urls_id:
        d[u.id] = {}
        data_by_url_id = ParseData.query.filter_by(url_id=u.id)
        for data in data_by_url_id:
            d[u.id][data.added_at] = {
                'stars': data.stars,
                'fork': data.fork,
                'last_commit': data.last_commit,
                'last_release': data.last_release
            }

    # create JSON file
    with open("sample.json", "w") as f:
        json.dump(d, f)

    return 'bla bla'