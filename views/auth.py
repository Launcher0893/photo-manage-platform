from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db import db
from models import Admin, Photographer, User
from utils.encryption import md5_encrypt, password_needs_upgrade, verify_password


bp = Blueprint('auth', __name__, url_prefix='/auth')


def load_user(user_id: str):
    if not user_id:
        return None

    prefix, _, raw_id = user_id.partition(':')
    if raw_id.isdigit():
        if prefix == 'admin':
            return db.session.get(Admin, int(raw_id))
        if prefix == 'user':
            return db.session.get(User, int(raw_id))

    if user_id.isdigit():
        return db.session.get(User, int(user_id))

    return None


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = db.session.execute(
            select(User).where(User.username == username)
        ).scalar_one_or_none()

        if user is None or not verify_password(user.password, password):
            flash('用户名或密码错误。', 'error')
            return render_template('login.html')
        if user.status != 1:
            flash('该账号已被禁用。', 'error')
            return render_template('login.html')

        if password_needs_upgrade(user.password, password):
            user.password = md5_encrypt(password)
            db.session.commit()

        login_user(user)
        flash('登录成功。', 'success')
        return redirect(url_for('index'))

    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        nickname = request.form.get('nickname', '').strip()
        user_role = request.form.get('user_role', type=int, default=User.ROLE_NORMAL)

        if not username or not password:
            flash('用户名和密码不能为空。', 'error')
            return render_template('register.html')
        if password != confirm_password:
            flash('两次输入的密码不一致。', 'error')
            return render_template('register.html')
        if user_role not in (User.ROLE_NORMAL, User.ROLE_PHOTOGRAPHER):
            user_role = User.ROLE_NORMAL

        existing_user = db.session.execute(
            select(User).where(User.username == username)
        ).scalar_one_or_none()
        if existing_user is not None:
            flash('用户名已存在。', 'error')
            return render_template('register.html')

        user = User(
            username=username,
            password=md5_encrypt(password),
            nickname=nickname or username,
            user_role=user_role,
            status=1,
        )
        db.session.add(user)

        try:
            db.session.flush()
            if user_role == User.ROLE_PHOTOGRAPHER:
                db.session.add(
                    Photographer(
                        user_id=user.user_id,
                        cert_status=Photographer.STATUS_PENDING,
                    )
                )
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('注册失败，请稍后重试。', 'error')
            return render_template('register.html')

        flash('注册成功，请登录。', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@bp.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_account = request.form.get('admin_account', '').strip()
        admin_password = request.form.get('admin_password', '')
        admin = db.session.execute(
            select(Admin).where(Admin.admin_account == admin_account)
        ).scalar_one_or_none()

        if admin is None or not verify_password(admin.admin_password, admin_password):
            flash('管理员账号或密码错误。', 'error')
            return render_template('admin_login.html')
        if admin.status != 1:
            flash('该管理员账号已被禁用。', 'error')
            return render_template('admin_login.html')

        if password_needs_upgrade(admin.admin_password, admin_password):
            admin.admin_password = md5_encrypt(admin_password)
            db.session.commit()

        login_user(admin)
        flash('管理员登录成功。', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('admin_login.html')


@bp.route('/logout')
@login_required
def logout():
    is_admin = getattr(current_user, 'is_admin', False)
    logout_user()
    flash('已退出登录。', 'success')
    if is_admin:
        return redirect(url_for('auth.admin_login'))
    return redirect(url_for('index'))
