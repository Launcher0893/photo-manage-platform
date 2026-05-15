"""权限装饰器工具。

装饰器就是写在函数上方的 @xxx。
本文件提供两个常用装饰器：
- @admin_required：只有管理员能访问。
- @user_required：只有普通用户/摄影师用户能访问，管理员不能访问。

这些装饰器会先做权限检查，检查通过后才执行真正的视图函数。
"""

from functools import wraps

from flask import abort, flash, redirect, url_for
from flask_login import current_user, logout_user


def admin_required(view_func):
    """后台管理员权限检查。

    用法示例：
        @admin_bp.route('/list')
        @admin_required
        def admin_list():
            ...

    访问流程：
    1. 没登录 -> 跳转 /auth/login。
    2. 登录了但不是管理员 -> 403。
    3. 管理员账号被禁用 -> 退出登录并跳转登录页。
    4. 检查通过 -> 执行原来的 view_func。
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if not getattr(current_user, 'is_admin', False):
            abort(403)
        if getattr(current_user, 'status', 0) != 1:
            logout_user()
            flash('账号已被禁用，请联系管理员。', 'error')
            return redirect(url_for('auth.login'))
        return view_func(*args, **kwargs)

    return wrapper


def user_required(view_func):
    """前台用户权限检查。

    用于普通用户和摄影师用户页面，例如 /work/add、/forum/my、/user/profile。
    它只保证“已登录且不是管理员”，具体是不是认证摄影师，需要业务函数内部继续判断。
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if getattr(current_user, 'is_admin', False):
            abort(403)
        if getattr(current_user, 'status', 0) != 1:
            logout_user()
            flash('账号已被禁用，请联系管理员。', 'error')
            return redirect(url_for('auth.login'))
        return view_func(*args, **kwargs)

    return wrapper
