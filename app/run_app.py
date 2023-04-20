from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='sfsdfw234sd23rwd23rwd23',
    SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://kts_user:kts_pass@localhost:5432/flask"
)
db = SQLAlchemy()
db.init_app(app)

# blueprint

from app.parser import parser
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

from app.models import *

with app.app_context():
    db.create_all()

#     # app.config.from_pyfile('config.py', silent=True)
#
#     # try:
#     #     os.makedirs(app.instance_path)
#     # except OSError:
#     #     pass
#
