from flask import Blueprint, render_template
from flask_login import current_user

from utils.demo_data import Pagination, posts, user_normal, user_photographer


bp = Blueprint('user', __name__, url_prefix='/user')
admin_bp = Blueprint('admin_user', __name__, url_prefix='/admin/user')


@bp.route('/profile')
def profile():
    my_posts = [post for post in posts if post.user.user_id == getattr(current_user, 'user_id', user_normal.user_id)]
    return render_template('user/profile.html', posts=my_posts)


@bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    return render_template('user/edit_profile.html')


@bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    return render_template('user/change_password.html')


@admin_bp.route('/list')
def admin_list():
    users = [user_normal, user_photographer]
    return render_template('user/admin_list.html', users=Pagination(users))
