import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from parser.run_app import User, db

# from flaskr.db import get_db

# bp = Blueprint('auth', __name__, url_prefix='/auth')
bp = Blueprint('auth', __name__)


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # db = get_db()
        # error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

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
