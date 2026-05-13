from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db import db
from models import ForumPost, User, WorkComment
from utils.decorators import admin_required, user_required
from utils.file_upload import delete_uploaded_file, save_image
from utils.logger import log_admin_action


bp = Blueprint('user', __name__, url_prefix='/user')
admin_bp = Blueprint('admin_user', __name__, url_prefix='/admin/user')


@bp.route('/profile')
@user_required
def profile():
    my_posts = db.session.execute(
        select(ForumPost)
        .options(joinedload(ForumPost.forum_board))
        .where(ForumPost.user_id == current_user.user_id, ForumPost.status == 1)
        .order_by(ForumPost.create_time.desc(), ForumPost.post_id.desc())
    ).scalars().all()
    return render_template('user/profile.html', posts=my_posts)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@user_required
def edit_profile():
    if request.method == 'POST':
        old_avatar_url = None
        current_user.nickname = request.form.get('nickname', '').strip() or current_user.username
        current_user.email = request.form.get('email', '').strip() or None
        current_user.phone = request.form.get('phone', '').strip() or None
        try:
            avatar_url = save_image(request.files.get('avatar_file'), 'avatars')
            if avatar_url:
                old_avatar_url = current_user.avatar_url
                current_user.avatar_url = avatar_url
        except ValueError as exc:
            flash(str(exc), 'error')
            return render_template('user/edit_profile.html')
        db.session.commit()
        delete_uploaded_file(old_avatar_url)
        flash('个人资料已更新。', 'success')
        return redirect(url_for('user.profile'))
    return render_template('user/edit_profile.html')


@bp.route('/change_password', methods=['GET', 'POST'])
@user_required
def change_password():
    from utils.encryption import md5_encrypt

    if request.method == 'POST':
        old_password = request.form.get('old_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        if current_user.password != md5_encrypt(old_password):
            flash('原密码错误。', 'error')
            return render_template('user/change_password.html')
        if not new_password or new_password != confirm_password:
            flash('新密码不能为空，且两次输入必须一致。', 'error')
            return render_template('user/change_password.html')
        current_user.password = md5_encrypt(new_password)
        db.session.commit()
        flash('密码已修改。', 'success')
        return redirect(url_for('user.profile'))
    return render_template('user/change_password.html')


@admin_bp.route('/list')
@admin_required
def admin_list():
    page = request.args.get('page', default=1, type=int)
    username = request.args.get('username', '').strip()
    nickname = request.args.get('nickname', '').strip()
    user_role = request.args.get('user_role', type=int)
    status = request.args.get('status', type=int)

    stmt = select(User).order_by(User.create_time.desc(), User.user_id.desc())
    if username:
        stmt = stmt.where(User.username.like(f'%{username}%'))
    if nickname:
        stmt = stmt.where(User.nickname.like(f'%{nickname}%'))
    if user_role in (User.ROLE_NORMAL, User.ROLE_PHOTOGRAPHER):
        stmt = stmt.where(User.user_role == user_role)
    if status in (0, 1):
        stmt = stmt.where(User.status == status)

    users = db.paginate(stmt, page=page, per_page=10, error_out=False)
    return render_template('user/admin_list.html', users=users)


@admin_bp.route('/detail/<int:user_id>')
@admin_required
def detail(user_id):
    user = db.session.execute(
        select(User)
        .options(joinedload(User.photographer))
        .where(User.user_id == user_id)
    ).scalar_one_or_none()
    if user is None:
        flash('用户不存在。', 'error')
        return redirect(url_for('admin_user.admin_list'))

    posts = db.session.execute(
        select(ForumPost)
        .options(joinedload(ForumPost.forum_board))
        .where(ForumPost.user_id == user_id)
        .order_by(ForumPost.create_time.desc(), ForumPost.post_id.desc())
        .limit(10)
    ).scalars().all()
    comments = db.session.execute(
        select(WorkComment)
        .options(joinedload(WorkComment.photo_work))
        .where(WorkComment.user_id == user_id)
        .order_by(WorkComment.create_time.desc(), WorkComment.comment_id.desc())
        .limit(10)
    ).scalars().all()
    photographer = user.photographer
    return render_template(
        'user/admin_detail.html',
        user=user,
        photographer=photographer,
        posts=posts,
        comments=comments,
    )


@admin_bp.route('/status/<int:user_id>')
@admin_required
def toggle_status(user_id):
    user = db.session.get(User, user_id)
    if user is not None:
        user.status = 0 if user.status == 1 else 1
        db.session.commit()
        log_admin_action('用户状态', f'更新用户状态：{user.username}')
        flash('用户状态已更新。', 'success')
    return redirect(url_for('admin_user.admin_list'))
