from flask_login import UserMixin

from app.run_app import db


# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
# app.db = SQLAlchemy() - Pycharm на это ругается. хотя я не проверял правда ли будет ошибка
# для миграций подключить Alembic - https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#create-the-tables


class User(db.Model, UserMixin):  # Затем убрать все db.что-то там за счет прямого импорта.
    # Смотри -- https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/models/#defining-models
    """
    checked in business-logic
        username UNIQUE and NOT NULL
        password NOT NULL
        email UNIQUE and NOT NULL
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)
    is_email_confirmed = db.Column(db.Boolean, default=False)

    pill_requests = db.relationship('PullRequest')


class PullRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.ForeignKey(User.id))
    start_date = db.Column(db.Date, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    actual_qty = db.Column(db.Integer, default=0)


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pull_request_id = db.Column(db.ForeignKey(PullRequest.id))
    url = db.Column(db.String, nullable=False)


class ParseData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.ForeignKey(Url.id))
    added_at = db.Column(db.String, nullable=False)
    stars = db.Column(db.String, nullable=False)
    fork = db.Column(db.String, nullable=False)
    last_commit = db.Column(db.String)
    last_release = db.Column(db.String)

# DROP TABLE parse_data;
# DROP TABLE url;
# DROP TABLE pull_request;
# DROP TABLE "user";
