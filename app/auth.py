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
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import User
from app.run_app import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        print(user)
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('parser.parcing_lists_page', user=current_user))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Usermane does not exist', category='error')

    return render_template('auth/login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=('GET', 'POST'))
def register():
    def chech_data(username, password, password_repeat, email):
        error = None
        if not username:
            error = 'Username is required'
        elif not password or not password_repeat:
            error = 'Password and "Repeat password" are required'
        elif password != password_repeat:
            error = 'Passwords are not the same'
        else:
            user_from_db = User.query.filter_by(username=username).first()
            email_from_db = User.query.filter_by(email=email).first()

            if user_from_db:
                error = 'Username already exists'
            elif email_from_db:
                error = 'Email already exists'

        return error

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_repeat = request.form['password_repeat']
        email = request.form['email']

        error = chech_data(username, password, password_repeat, email)
        if error:
            flash(error, category='error')
        else:
            new_user = User(username=username,
                            password=generate_password_hash(password, method='sha256'),
                            email=email)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('parser.parcing_lists_page', user=current_user))

    return render_template('auth/register.html', user=current_user)
