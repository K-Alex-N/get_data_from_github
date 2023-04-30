import datetime

from flask import flash
from flask_login import current_user

from app.run_app import db, app
from app.store.db.models import PullRequest, Url


def create_pull_request(name, links):
    with app.app_context():
        try:
            pull_request = PullRequest(
                name=name,
                user_id=current_user.id,
                start_date=datetime.datetime.now(),  # вот это можно перенести прямо в класс!!!
            )
            db.session.add(pull_request)
            db.session.flush()

            for link in links:
                url = Url(pull_request_id=pull_request.id, url=link)
                db.session.add(url)
            db.session.commit()

            return pull_request.id

        except:
            flash('Обшибка добавления в БД', category='error')
