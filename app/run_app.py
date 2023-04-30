import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='sfsdfw234sd23rwd23rwd23',
    SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://kts_user:kts_pass@localhost:5432/flask",
    SCHEDULER_API_ENABLED=True,
    SCHEDULER_TIMEZONE = "Europe/London",
)
db = SQLAlchemy()
db.init_app(app)

# Blueprint
from app.parser import parser, parse_urls
from app.auth import auth
from app.error import error

app.register_blueprint(parser, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(error, url_prefix='/')

# Flask-login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# create DB
from app.store.db.models import *

with app.app_context():
    db.create_all()

# APScheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@scheduler.task('interval', seconds=10000)
# @scheduler.task('cron', minute=0, hour=0, day='*')
def everyday_parsing():
    with scheduler.app.app_context():
        urls = Url.query.all()
        if not parse_urls(urls):
            # отправлять алерт на почту
            pass

@scheduler.task('cron', hour=23, minute=59, day='*')
# @scheduler.task('interval', seconds=2)
def everyday_delete_JSONs():
    with scheduler.app.app_context():
        json_path = "app/data/json"
        for f in os.listdir(path=json_path):
            os.remove(json_path + '/' + f)


#     # app.config.from_pyfile('config.py', silent=True)
#
#     # try:
#     #     os.makedirs(app.instance_path)
#     # except OSError:
#     #     pass
#
