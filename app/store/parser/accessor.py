import datetime

from flask import flash
from flask_login import current_user

from app.run_app import db, app
from app.store.db.models_w_flsak_alchemy import PullRequest, Url


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
            pass


def get_urls_by_pull_request_id(pull_request_id):
    # urls = Url.query.filter_by(pull_request_id=pull_request_id).all()
    # with app.app_context():
    #     try:
    #         urls = execute.scalar(select(Url).where(Url.pull_request_id=pull_request_id))
    pass