import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from sqlalchemy import select

from app.parser.utils import parse_urls
from app.store.db import User, session, Url
from config.config import PATH_TO_JSON

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='sfsdfw234sd23rwd23rwd23',
    SCHEDULER_API_ENABLED=True,
    SCHEDULER_TIMEZONE="Europe/London",
)

# Blueprint
from app.parser.routes import parser
from app.auth.routes import auth

app.register_blueprint(parser, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

# Flask-login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return session.scalar(select(User).where(User.id == int(id)))


# APScheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@scheduler.task('interval', seconds=10000)
# @scheduler.task('cron', minute=0, hour=0, day='*')
def everyday_parsing():
    with scheduler.app.app_context():
        urls = session.scalars(select(Url))
        if not parse_urls(urls):
            # отправлять алерт на почту
            pass


@scheduler.task('cron', hour=23, minute=59, day='*')
# @scheduler.task('interval', seconds=2)
def everyday_delete_JSONs():
    with scheduler.app.app_context():
        for f in os.listdir(path=PATH_TO_JSON):
            os.remove(PATH_TO_JSON + '/' + f)


# Error handlers
@app.errorhandler(500)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/page404.html'), 404

#     # app.config.from_pyfile('config.py', silent=True)
#
#     # try:
#     #     os.makedirs(app.instance_path)
#     # except OSError:
#     #     pass
#
