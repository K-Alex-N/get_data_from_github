import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.run_app import User, db

# from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')



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
    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'

    user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one()



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


            new_user = User(
                login=username,
                password=password,
                email=request.form['email']
            )

            db.session.add(new_user)
            db.session.commit()

            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')