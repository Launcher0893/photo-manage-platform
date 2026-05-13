from functools import wraps

from flask import abort, redirect, url_for
from flask_login import current_user


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if not getattr(current_user, 'is_admin', False):
            abort(403)
        return view_func(*args, **kwargs)

    return wrapper


def user_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if getattr(current_user, 'is_admin', False):
            abort(403)
        return view_func(*args, **kwargs)

    return wrapper
