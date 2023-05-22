from flask import Blueprint
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import render_template
from flask_login import login_required
from flask_login import login_user
from flask_login import current_user
from flask_login import logout_user
from werkzeug.security import generate_password_hash
from sqlalchemy import select

from app.auth.utils import is_login_data_valid, is_registration_data_valid
from app.db import try_except_session, session
from app.db import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember_me = True if request.form.get('remember_me') else False

        if is_login_data_valid(username, password):
            login_user(session.scalar(select(User).where(User.username == username)),
                       remember=remember_me)
            flash('Logged in successfully!', category='success')
            return redirect(url_for('parser.home', user=current_user))

    return render_template('auth/login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_repeat = request.form['password_repeat']
        email = request.form['email']

        if is_registration_data_valid(username, password, password_repeat, email):
            new_user = User(username=username,
                            password=generate_password_hash(password, method='sha256'),
                            email=email)
            with try_except_session() as session:
                session.add(new_user)
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('parser.home', user=current_user))

    return render_template('auth/register.html', user=current_user)
