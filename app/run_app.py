import datetime

from flask import Flask, render_template, request, flash

# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# app.db = SQLAlchemy()
db = SQLAlchemy()

app.config.from_mapping(
    SECRET_KEY=Flask.secret_key,
    SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://kts_user:kts_pass@localhost:5432/kts"
)
db.init_app(app)


class User(
    db.Model):  # Затем убрать все db.что-то там за счет прямого импорта. Смотри -- https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/models/#defining-models
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
    # app = create_app()

    @app.route('/')
    def parcing_lists_page():
        # return render_template('parcing_lists.html')
        return render_template('base.html')

    # @app.route('/<int:parcing_id>')
    # def parcing_data_page(parcing_id):
    #     return render_template('parcing_lists.html')

    @app.route('/login')
    def login():
        return render_template('auth/login.html')

    @app.route('/register')
    def register():
        return render_template('auth/register.html')

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('exeption/page404.html'), 404

    def check_data(form):
        res = []
        if not form['name']:
            res.append('введите название')
        links = form['links']
        if not links:
            res.append('введите ссылки на репозитории')
        else:
            for link in links:
                if 'https://github.com' not in link:
                    res.append('пожалуйста введите полную ссылку на репозиторий (начинается с https://github.com)')
                    break
        return '\n'.join(res)

    @app.route('/add', methods=['POST', 'GET'])
    def add_new_parcing():
        if request.method == 'POST':
            err = check_data(request.form)
            if err:
                flash(err)
                return render_template('app/add_new_parcing.html')

            pull_request = PullRequest(
                name=request.form['name'],
                start_date=datetime.datetime.now(),
                frequency=request.form['frequency'],
            )
            db.session.add(pull_request)
            db.session.commit()

            for link in request.form['links'].split():
                url = Url(
                    pull_request_id=pull_request.id,
                    url=link
                )
                db.session.add(url)
            db.session.commit()
            # дб пересылка на страницу пользователя, а точнее на страницу данного задания на парсинг в странице пользователя
            # return redirect(url_for("parse_details", id=pull_request.id))

        return render_template('app/add_new_parcing.html')

    app.run()

    # run_db()
