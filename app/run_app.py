import os

from flask import Flask, render_template, request, flash

import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='JdjhD&@281J',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)
db.init_app(app)

class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    type = sa.Column(sa.String)

with app.app_context():
    db.create_all()

parsing = db.


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
#     return app


def run_app():
    app = create_app()

    @app.route('/')
    def parcing_lists_page():
        # return render_template('parcing_lists.html')
        return render_template('base.html')

    # @app.route('/<int:parcing_id>')
    # def parcing_data_page(parcing_id):
    #     return render_template('parcing_lists.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('page404.html'), 404

    @app.route('/add', methods=['POST', 'GET'])
    def add_new_parcing():
        if request.method == 'POST':
            if len(request.form['scrapper_name']) < 2:
                flash('Название должно иметь минимум 2 символа')
            if not request.form['links']:
                flash('Введите хотябы одну ссылку')

        return render_template('add_new_parcing.html')

    app.run()

    # run_db()
