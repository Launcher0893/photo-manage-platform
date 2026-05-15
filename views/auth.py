"""登录、注册、退出模块。

蓝图前缀：/auth
主要页面：
- /auth/login：普通用户和管理员共用登录页。
- /auth/register：普通用户/摄影师注册。
- /auth/logout：退出登录。

本文件还提供 load_user()，给 app.py 中 Flask-Login 的 user_loader 回调用。
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db import db
from models import Admin, Photographer, User
from utils.encryption import md5_encrypt, password_needs_upgrade, verify_password


bp = Blueprint('auth', __name__, url_prefix='/auth')


def load_user(user_id: str):
    """根据 Flask-Login 保存的登录 id 重新加载用户对象。

    User.get_id() 返回 user:<id>，Admin.get_id() 返回 admin:<id>。
    所以这里通过前缀判断应该查 user 表还是 admin 表。
    """
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
    """统一登录页：完整访问地址 /auth/login。

    GET：打开登录页面 templates/login.html。
    POST：接收表单账号密码，先查普通用户 user 表，再查管理员 admin 表。
    登录成功后：
    - 普通用户跳转首页 index -> /
    - 管理员跳转 dashboard.index -> /admin/dashboard/
    """
    if current_user.is_authenticated:
        if getattr(current_user, 'is_admin', False):
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('index'))

    if request.method == 'POST':
        # request.form 表示 HTML 表单提交过来的数据。
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # 先尝试按普通用户登录。
        user = db.session.execute(
            select(User).where(User.username == username)
        ).scalar_one_or_none()
        if user is not None and verify_password(user.password, password):
            if user.status != 1:
                flash('该账号已被禁用。', 'error')
                return render_template('login.html')

            if password_needs_upgrade(user.password, password):
                user.password = md5_encrypt(password)
                db.session.commit()

            # login_user() 会把用户 id 写入 session，后续 current_user 就能拿到当前用户。
            login_user(user)
            flash('登录成功。', 'success')
            return redirect(url_for('index'))

        # 普通用户不匹配时，再尝试按管理员账号登录。
        admin = db.session.execute(
            select(Admin).where(Admin.admin_account == username)
        ).scalar_one_or_none()
        if admin is not None and verify_password(admin.admin_password, password):
            if admin.status != 1:
                flash('该管理员账号已被禁用。', 'error')
                return render_template('login.html')

            if password_needs_upgrade(admin.admin_password, password):
                admin.admin_password = md5_encrypt(password)
                db.session.commit()

            login_user(admin)
            flash('管理员登录成功。', 'success')
            return redirect(url_for('dashboard.index'))

        flash('账号或密码错误。', 'error')
        return render_template('login.html')

    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """注册页：完整访问地址 /auth/register。

    GET：打开 templates/register.html。
    POST：创建 user 记录；如果选择摄影师角色，同时创建 photographer 待审核记录。
    """
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

        # 注册前先检查用户名是否已存在。
        existing_user = db.session.execute(
            select(User).where(User.username == username)
        ).scalar_one_or_none()
        if existing_user is not None:
            flash('用户名已存在。', 'error')
            return render_template('register.html')

        # 创建用户对象。此时还只是 Python 对象，db.session.add 后才准备写入数据库。
        user = User(
            username=username,
            password=md5_encrypt(password),
            nickname=nickname or username,
            user_role=user_role,
            status=1,
        )
        db.session.add(user)

        try:
            # flush 会先把 user 插入数据库，从而拿到自增的 user.user_id。
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
    """旧管理员登录入口。

    为了兼容旧地址，访问 /auth/admin_login 会跳到统一登录页 /auth/login。
    """
    return redirect(url_for('auth.login'))


@bp.route('/logout')
@login_required
def logout():
    """退出登录：清除当前 session，然后跳回登录页。"""
    logout_user()
    flash('已退出登录。', 'success')
    return redirect(url_for('auth.login'))
