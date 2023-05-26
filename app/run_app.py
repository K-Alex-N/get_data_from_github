import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from sqlalchemy import select

from app.parser.utils import parse_urls
from app.db import User, session, Url
from config.config import JSON_DIR, secret_key

# ---------------------------------------------------------------- #
# app
# ---------------------------------------------------------------- #
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
# ---------------------------------------------------------------- #
# Blueprints
# ---------------------------------------------------------------- #
from app.parser.routes import parser
from app.auth.routes import auth

app.register_blueprint(parser, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
# ---------------------------------------------------------------- #
# Flask-login
# ---------------------------------------------------------------- #
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return session.scalar(select(User).where(User.id == int(id)))


# ---------------------------------------------------------------- #
# APScheduler
# ---------------------------------------------------------------- #
app.config.update(
    SCHEDULER_API_ENABLED=True,
    SCHEDULER_TIMEZONE="Europe/London"
)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@scheduler.task('cron', minute=0, hour=0, day='*')
# @scheduler.task('interval', seconds=10000)
def everyday_parsing():
    with scheduler.app.app_context():
        urls = session.scalars(select(Url))
        if not parse_urls(urls):
            pass # отправлять алерт на почту?


@scheduler.task('cron', hour=23, minute=59, day='*')
# @scheduler.task('interval', seconds=2)
def everyday_delete_JSONs():
    with scheduler.app.app_context():
        for file in os.listdir(path=JSON_DIR):
            os.remove(os.path.join(JSON_DIR, file))


# ---------------------------------------------------------------- #
# Error handlers
# ---------------------------------------------------------------- #
@app.errorhandler(500)
@app.errorhandler(404)
def error(e):
    return render_template('error/page404.html'), 404


@app.errorhandler(403)
def error(e):
    return render_template('error/page403.html'), 403
