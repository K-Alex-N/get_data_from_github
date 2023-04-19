import datetime

from flask import Flask
from flask import flash
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='sfsdfw234sd23rwd23rwd23',
    SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://kts_user:kts_pass@localhost:5432/kts"
)
db = SQLAlchemy()
db.init_app(app)


@app.route('/')
def parcing_lists_page():
    # return render_template('parcing_lists.html')
    return render_template('base.html')


# @app.route('/<int:parcing_id>')
# def parcing_data_page(parcing_id):
#     return render_template('parcing_lists.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('exeption/page404.html'), 404


def check_data(form):
    error = []
    if not form['name']:
        error.append('введите название')
    links = form['links']
    if not links:
        error.append('введите ссылки на репозитории')
    else:
        for link in links:
            if 'https://github.com' not in link:
                error.append('введите полную ссылку на репозиторий (пример https://github.com/django/django)')
                break
    return '\n'.join(error)


@app.route('/add', methods=['POST', 'GET'])
def add_new_parcing():
    if request.method == 'POST':
        error = check_data(request.form)
        if error:
            flash(error)
            return render_template('app/add_new_parcing.html')

        try:
            pull_request = PullRequest(
                name=request.form['name'],
                start_date=datetime.datetime.now(),  # вот это можно перенести прямо в класс!!!
                frequency=request.form['frequency'],
            )
            db.session.add(pull_request)
            db.session.commit()  # попробовать db.session.flush() !!!

            for link in request.form['links'].split():
                url = Url(
                    pull_request_id=pull_request.id,
                    url=link
                )
                db.session.add(url)
            db.session.commit()
        except:
            db.session.rollback()
            print('Обшибка добавления в БД')
        # дб пересылка на страницу пользователя, а точнее на страницу данного задания на парсинг в странице пользователя
        # return redirect(url_for("parse_details", id=pull_request.id))

    return render_template('app/add_new_parcing.html')


# ----------------------------------------------------------------#
#                          AUTH
# ----------------------------------------------------------------#
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # db = get_db()

        # user = db.execute(
        #     'SELECT * FROM user WHERE username = ?', (username,)
        # ).fetchone()

        error = None
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

def chech_register_data(username, password, email):
    user_from_db = db.session.execute(db.select(User).where(username=username)).scalar_one()
    # может быть так?
    # user_from_db = User.query.where(username=username).first()
    email_from_db = db.session.execute(db.select(User).where(email=email)).scalar_one()

    error = None
    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    elif username == user_from_db:
        error = 'Username already exists.'
    elif email == email_from_db:
        error = 'Email already exists.'

    return error


@app.route('/register')
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        error = chech_register_data(username, password, email)
        if error:
            flash(error)
            return redirect

        db.session.add(User(login=username, password=password, email=email))
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template('auth/register.html')



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
