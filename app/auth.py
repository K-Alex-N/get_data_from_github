from flask import Blueprint
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import render_template

from werkzeug.security import check_password_hash

from app.models import User
from app.run_app import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=('GET', 'POST'))
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


@auth.route('/register')
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
