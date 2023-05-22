from flask import flash
from sqlalchemy import select
from werkzeug.security import check_password_hash

from app.db import session, User


def is_login_data_valid(username, password):
    user = session.scalar(select(User).where(User.username == username))
    if not user:
        flash('Username does not exist', category='error')
        return False

    if not check_password_hash(user.password, password):
        flash('Incorrect password, try again', category='error')
        return False

    return True


def is_registration_data_valid(username, password, password_repeat, email):
    if not username:
        flash('Username is required', category='error')
        return False

    if not password or not password_repeat:
        flash('Password and "Repeat password" are required', category='error')
        return False

    if len(password) < 8 or len(password_repeat) < 8:
        flash('Password should be >= 8 characters', category='error')
        return False

    if password != password_repeat:
        flash('Passwords are not the same', category='error')
        return False

    if session.scalar(select(User).where(User.username == username)):
        flash('Username already exists', category='error')
        return False

    if session.scalar(select(User).where(User.email == email)):
        flash('Email already exists', category='error')
        return False

    return True
