from flask_sqlalchemy import SQLAlchemy

from app.run_app import get_app

db = SQLAlchemy()
app = get_app()
db.init_app(app)

# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

# app.db = SQLAlchemy() - Pycharm на это ругается. хотя я не проверял правда ли будет ошибка

# для миграций подключить Alembic - https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#create-the-tablesы
class User(db.Model):  # Затем убрать все db.что-то там за счет прямого импорта.
    # Смотри -- https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/models/#defining-models
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    is_email_confirmed = db.Column(db.Boolean, default=False)

class PullRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.ForeignKey(User.id))  # maybe need to add "db.Integer"
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

with app.app_context():
    db.create_all()