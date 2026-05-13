from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from utils.demo_data import get_admin, get_user


bp = Blueprint('auth', __name__, url_prefix='/auth')


def load_mock_user(user_id: str):
    if not user_id:
        return None
    prefix, _, raw_id = user_id.partition(':')
    if not raw_id.isdigit():
        return None
    if prefix == 'admin':
        return get_admin()
    if prefix == 'user':
        return get_user(int(raw_id))
    return None


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = get_user(1)
        login_user(user)
        flash('登录成功', 'success')
        return redirect(url_for('index'))
    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        flash('当前为演示环境，注册功能后续接入数据库。', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')


@bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        login_user(get_admin())
        flash('管理员登录成功', 'success')
        return redirect(url_for('dashboard.index'))
    return render_template('admin_login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录', 'success')
    return redirect(url_for('index'))
