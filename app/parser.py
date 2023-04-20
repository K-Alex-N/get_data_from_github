import datetime

from flask import Blueprint, redirect, url_for
from flask import request
from flask import flash
from flask import render_template
from flask_login import current_user, login_user, login_required

from app.models import PullRequest, Url
from app.run_app import db

parser = Blueprint('parser', __name__)


@parser.route('/')
def parcing_lists_page():
    pull_requests = PullRequest.query.all()
    for rqst in pull_requests:
        name = rqst.name
        start_date = rqst.start_date
        frequency = rqst.frequency

    return render_template('app/parsing_lists.html')


# @parser.route('/<int:parcing_id>')
# def parcing_data_page(parcing_id):
#     return render_template('parsing_lists.html')


def check_data(name, links):
    error = None
    if not name:
        error = 'введите название'
    elif not links:
        error = 'введите ссылки на репозитории'
    else:
        for link in links.split():
            if 'github.com' not in link:
                print(link)
                error = 'введите полную ссылку на репозиторий (пример https://github.com/django/django)'
                break
    return error


@parser.route('/add', methods=['POST', 'GET'])
@login_required
def add_new_parcing():  # DONE!!!
    if request.method == 'POST':
        name = request.form.get('name')
        links = request.form.get('links')
        frequency = int(request.form.get('frequency'))

        error = check_data(name, links)
        if error:
            flash(error)
        else:
            try:
                pull_request = PullRequest(
                    name=name,
                    user_id=current_user.id,
                    start_date=datetime.datetime.now(),  # вот это можно перенести прямо в класс!!!
                    frequency=frequency,
                )
                db.session.add(pull_request)
                db.session.flush()

                for link in request.form['links'].split():
                    url = Url(
                        pull_request_id=pull_request.id,
                        url=link
                    )
                    db.session.add(url)
                db.session.commit()
                return redirect(url_for('parser.parcing_lists_page'))
            except:
                db.session.rollback()
                print('Обшибка добавления в БД')
            # дб пересылка на страницу пользователя, а точнее на страницу данного задания на парсинг в странице пользователя
            # return redirect(url_for("parse_details", id=pull_request.id))

    return render_template('app/add_new_parcing.html')
