"""用户中心和后台用户管理模块。

前台蓝图前缀：/user
后台蓝图前缀：/admin/user

本文件负责：
- 个人中心 /user/profile。
- 编辑个人资料、完善摄影师资料、修改密码。
- 后台用户列表、用户详情、禁用/启用、软删除、恢复。
"""

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db import db
from models import ForumPost, PhotoWork, Photographer, User, WorkComment
from utils.decorators import admin_required, user_required
from utils.file_upload import delete_uploaded_file, save_image
from utils.logger import log_admin_action


bp = Blueprint('user', __name__, url_prefix='/user')
admin_bp = Blueprint('admin_user', __name__, url_prefix='/admin/user')


@bp.route('/profile')
@user_required
def profile():
    """个人中心：完整访问地址 /user/profile。

    查询当前用户的摄影师资料、我的作品和我的帖子，
    然后渲染 templates/user/profile.html。
    """
    photographer = current_user.photographer if current_user.user_role == User.ROLE_PHOTOGRAPHER else None
    my_works = []
    if photographer is not None and photographer.cert_status == Photographer.STATUS_APPROVED:
        my_works = db.session.execute(
            select(PhotoWork)
            .options(joinedload(PhotoWork.category))
            .where(PhotoWork.photographer_id == photographer.photographer_id)
            .order_by(PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
        ).scalars().all()
    my_posts = db.session.execute(
        select(ForumPost)
        .options(joinedload(ForumPost.forum_board))
        .where(ForumPost.user_id == current_user.user_id, ForumPost.status == 1)
        .order_by(ForumPost.create_time.desc(), ForumPost.post_id.desc())
    ).scalars().all()
    return render_template('user/profile.html', posts=my_posts, photographer=photographer, works=my_works)


@bp.route('/edit_photographer', methods=['GET', 'POST'])
@user_required
def edit_photographer():
    """完善摄影师资料。

    GET：打开独立编辑页。
    POST：保存真实姓名和城市。
    当前个人中心也用弹窗表单提交到这个地址。
    """
    if current_user.user_role != User.ROLE_PHOTOGRAPHER:
        abort(403)

    photographer = current_user.photographer
    if photographer is None:
        photographer = Photographer(
            user_id=current_user.user_id,
            cert_status=Photographer.STATUS_PENDING,
        )

    if request.method == 'POST':
        db.session.add(photographer)
        photographer.real_name = request.form.get('real_name', '').strip() or None
        photographer.city = request.form.get('city', '').strip() or None
        if photographer.cert_status == Photographer.STATUS_REJECTED:
            photographer.cert_status = Photographer.STATUS_PENDING
            photographer.cert_remark = None
        db.session.commit()
        flash('摄影师资料已保存。', 'success')
        return redirect(url_for('user.profile'))

    return render_template('user/edit_photographer.html', photographer=photographer)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@user_required
def edit_profile():
    """编辑个人资料。

    修改昵称、邮箱、手机号和头像。
    头像上传调用 utils/file_upload.py 中的 save_image()。
    """
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
    """修改密码：校验旧密码，再把新密码保存为 MD5。"""
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
    """后台用户列表：完整访问地址 /admin/user/list。

    支持按用户名、昵称、角色、状态筛选。
    默认不显示 status=-1 的已删除用户。
    """
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
    if status in (-1, 0, 1):
        stmt = stmt.where(User.status == status)
    else:
        stmt = stmt.where(User.status != -1)

    users = db.paginate(stmt, page=page, per_page=10, error_out=False)
    return render_template('user/admin_list.html', users=users)


@admin_bp.route('/detail/<int:user_id>')
@admin_required
def detail(user_id):
    """后台用户详情：查看用户资料、摄影师资料、最近帖子和评论。"""
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


@admin_bp.route('/status/<int:user_id>', methods=['POST'])
@admin_required
def toggle_status(user_id):
    """后台启用/禁用用户。已删除用户不能直接启用或禁用。"""
    user = db.session.get(User, user_id)
    if user is not None:
        if user.status == -1:
            flash('已删除用户不能直接禁用或启用，请先恢复。', 'error')
            return redirect(url_for('admin_user.admin_list'))
        user.status = 0 if user.status == 1 else 1
        db.session.commit()
        log_admin_action('用户状态', f'更新用户状态：{user.username}')
        flash('用户状态已更新。', 'success')
    return redirect(url_for('admin_user.admin_list'))


@admin_bp.route('/delete/<int:user_id>', methods=['POST'])
@admin_required
def soft_delete(user_id):
    """后台软删除用户：把 user.status 改为 -1，不物理删除数据库记录。"""
    user = db.session.get(User, user_id)
    if user is not None:
        user.status = -1
        db.session.commit()
        log_admin_action('用户删除', f'删除用户：{user.username}')
        flash('用户已删除。', 'success')
    return redirect(url_for('admin_user.admin_list'))


@admin_bp.route('/restore/<int:user_id>', methods=['POST'])
@admin_required
def restore(user_id):
    """后台恢复已软删除用户：把 user.status 改回 1。"""
    user = db.session.get(User, user_id)
    if user is not None:
        user.status = 1
        db.session.commit()
        log_admin_action('用户恢复', f'恢复用户：{user.username}')
        flash('用户已恢复。', 'success')
    return redirect(url_for('admin_user.admin_list', status=-1))
