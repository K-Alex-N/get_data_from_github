import datetime
import os

from flask import Blueprint, redirect, url_for, send_from_directory, request, render_template
from flask_login import current_user, login_required
from sqlalchemy import select

from app.parser.utils import is_exist, delete_old_json_files, create_json, get_home_data, add_pull_request, \
    change_pull_request, is_user_valid
from app.db import session, try_except_session
from app.db import PullRequest, Url
from config.config import JSON_DIR

parser = Blueprint('parser', __name__)


# ---------------------------------------------------------------- #
# home page
# ---------------------------------------------------------------- #
@parser.route('/')
def home():
    data = get_home_data()
    return render_template('app/parser_list.html', user=current_user, data=data)


@parser.route('/add', methods=['POST', 'GET'])
@login_required
def add():
    if request.method == 'POST':
        add_pull_request(request)
        return redirect(url_for('parser.home', user=current_user))

    return render_template('app/parser_add.html', user=current_user)


@parser.route('/change/<int:pull_request_id>', methods=['POST', 'GET'])
@login_required
def change(pull_request_id):
    is_exist(pull_request_id)
    if request.method == 'POST':
        change_pull_request(request, pull_request_id)
        delete_old_json_files(pull_request_id)
        return redirect(url_for('parser.home', user=current_user))
    else:
        pull_request = session.scalar(select(PullRequest).where(PullRequest.id == pull_request_id))
        is_user_valid(pull_request.user_id)
        links = session.scalars(select(Url).where(Url.pull_request_id == pull_request.id)).all()
        str_links = '\n'.join([x.url for x in links])
        return render_template('app/parser_change.html', user=current_user, pr_name=pull_request.name, links=str_links)


@parser.route('/download_json/<int:pull_request_id>/<path:file_name>', methods=['POST', 'GET'])
def download_json(pull_request_id, file_name):
    is_exist(pull_request_id)
    file_path = os.path.join(JSON_DIR, str(pull_request_id))
    if not os.path.isfile(file_path):
        create_json(pull_request_id, file_path)

    return send_from_directory(JSON_DIR, str(pull_request_id),
                               as_attachment=True,
                               download_name=f'{file_name} {str(datetime.date.today())}.json'
                               )


@parser.route('/delete/<int:pull_request_id>', methods=['POST', 'GET'])
@login_required
def delete_parser(pull_request_id):
    is_exist(pull_request_id)
    with try_except_session() as session:
        pull_request = session.scalar(select(PullRequest).where(PullRequest.id == pull_request_id))
        is_user_valid(pull_request.user_id)
        session.delete(pull_request)
    return redirect(url_for('parser.home', user=current_user))


# ---------------------------------------------------------------- #
# other pages
# ---------------------------------------------------------------- #
@parser.route('/how_to_use')
def how_to_use():
    return render_template('app/how_to_use.html', user=current_user)


@parser.route('/about')
def about():
    return render_template('app/about.html', user=current_user)
