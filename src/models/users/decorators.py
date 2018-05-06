from functools import wraps
from src.config import ADMINS
from flask import session, url_for, redirect, request

__author__ = "esobolie"


def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        return func(*args, **kwargs)

    return decorated_function


def requires_admin_permissions(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        if session['email'] not in ADMINS:
            return redirect(url_for('users.login_user', message="You need to be an admin to access that"))
        return func(*args, **kwargs)

    return decorated_function
