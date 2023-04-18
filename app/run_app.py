import datetime

from flask import Flask, render_template, request, flash

# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from flask_sqlalchemy import SQLAlchemy




def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='sfsdfw234sd23rwd23rwd23',
        SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://kts_user:kts_pass@localhost:5432/kts"
    )

    from app import auth
    from app import parser
    app.register_blueprint(auth.bp)
    app.register_blueprint(parser.bp)

    # def create_app() -> Flask:
    #     app = Flask(__name__)
    #     app.config.from_mapping(
    #         SECRET_KEY='JdjhD&@281J',
    #         DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    #     )
    #
    #     # app.config.from_pyfile('config.py', silent=True)
    #
    #     # try:
    #     #     os.makedirs(app.instance_path)
    #     # except OSError:
    #     #     pass
    #

    return app


def create_db(app):
    # app.db = SQLAlchemy() - Pycharm на это ругается. хотя я не проверял правда ли будет ошибка
    db = SQLAlchemy()
    db.init_app(app)

    class User(db.Model):  # Затем убрать все db.что-то там за счет прямого импорта.
        # Смотри -- https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/models/#defining-models
        id = db.Column(db.Integer, primary_key=True)
        login = db.Column(db.String, unique=True, nullable=False)
        password = db.Column(db.String, unique=True, nullable=False)
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

    # для миграций подключить Alembic - https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#create-the-tablesы


def run_app():
    app = create_app()
    create_db(app)
    app.run()

    # run_db()
