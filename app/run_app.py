from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='sfsdfw234sd23rwd23rwd23',
    SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://kts_user:kts_pass@localhost:5432/kts"
)
db = SQLAlchemy()
db.init_app(app)

from app.parser import parser
from app.auth import auth

app.register_blueprint(parser, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

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
