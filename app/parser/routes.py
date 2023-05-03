import datetime
import os

from flask import Blueprint, redirect, url_for, send_from_directory, request, render_template
from flask_login import current_user, login_required
from sqlalchemy import select

from app.parser.utils import is_exist, add_or_change, delete_old_json_file, create_dict_by_pull_request_id, create_json
from app.store.db import session, try_except_session
from app.store.db.models import PullRequest, Url
from config.config import PATH_TO_JSON

parser = Blueprint('parser', __name__)


@parser.route('/')
def home():
    pull_requests = session.scalars(select(PullRequest)).all()
    url = session.scalars(select(Url)).all()
    data = []
    for pr in pull_requests:
        data.append([pr, [u for u in url if u.pull_request_id == pr.id]])

    return render_template('app/parsing_lists.html', user=current_user, data=data)



@parser.route('/add', methods=['POST', 'GET'])
@login_required
def add():
    if request.method == 'POST':
        add_or_change(request, 'add')
        return redirect(url_for('parser.home', user=current_user))

    return render_template('app/add_new_parsing.html', user=current_user)



@parser.route('/change/<int:pull_request_id>', methods=['POST', 'GET'])
@login_required
def change(pull_request_id):
    is_exist(pull_request_id)
    if request.method == 'POST':
        add_or_change(request, 'change', pull_request_id)
        delete_old_json_file(pull_request_id)
        return redirect(url_for('parser.home', user=current_user))
    else:
        pull_request = session.scalar(select(PullRequest).where(PullRequest.id == pull_request_id))
        links = session.scalars(select(Url).where(Url.pull_request_id == pull_request.id)).all()
        str_links = '\n'.join([x.url for x in links])
        return render_template('app/change.html', user=current_user, pr_name=pull_request.name, links=str_links)


@parser.route('/download_json/<int:pull_request_id>/<path:file_name>', methods=['POST', 'GET'])
def download_json(pull_request_id, file_name):
    is_exist(pull_request_id)
    file_path = os.path.join(PATH_TO_JSON, str(pull_request_id))
    if not os.path.isfile(file_path):
        create_json(pull_request_id, file_path)

    return send_from_directory(PATH_TO_JSON, str(pull_request_id),
                               as_attachment=True,
                               download_name=f'{file_name} {str(datetime.date.today())}.json'
                               )

@parser.route('/delete/<int:pull_request_id>', methods=['POST', 'GET'])
@login_required
def delete_parser(pull_request_id):
    is_exist(pull_request_id)
    with try_except_session() as session:
        pull_request = session.scalar(select(PullRequest).where(PullRequest.id == pull_request_id))
        session.delete(pull_request)
    return redirect(url_for('parser.home', user=current_user))


@parser.route('/how_to_use')
def how_to_use():
    return render_template('app/how_to_use.html', user=current_user)
