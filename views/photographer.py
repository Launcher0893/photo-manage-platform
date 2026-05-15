"""摄影师前台展示和后台审核模块。

前台蓝图前缀：/photographer
后台蓝图前缀：/admin/photographer

本文件负责：
- 摄影师列表和摄影师主页。
- 管理员审核摄影师认证资料。
"""

from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from db import db
from models import PhotoWork, Photographer, User
from utils.decorators import admin_required
from utils.logger import log_admin_action


bp = Blueprint('photographer', __name__, url_prefix='/photographer')
admin_bp = Blueprint('admin_photographer', __name__, url_prefix='/admin/photographer')


@bp.route('/list')
def list_page():
    """摄影师列表：完整访问地址 /photographer/list。

    只展示认证通过且用户状态正常的摄影师。
    支持按城市和昵称搜索。
    """
    page = request.args.get('page', default=1, type=int)
    city = request.args.get('city', '').strip()
    # 🔥 新增：获取昵称搜索参数
    nickname = request.args.get('nickname', '').strip()

    stmt = (
        select(Photographer)
        .options(joinedload(Photographer.user), selectinload(Photographer.works))
        .join(Photographer.user)
        .where(
            Photographer.cert_status == Photographer.STATUS_APPROVED,
            User.status == 1,
        )
        .order_by(Photographer.create_time.desc(), Photographer.photographer_id.desc())
    )

    if city:
        stmt = stmt.where(Photographer.city.like(f'%{city}%'))

    # 🔥 新增：按摄影师昵称（用户表）搜索
    if nickname:
        stmt = stmt.where(User.nickname.like(f'%{nickname}%'))

    photographers = db.paginate(stmt, page=page, per_page=9, error_out=False)
    return render_template('photographer/list.html', photographers=photographers)


@bp.route('/detail/<int:photographer_id>')
def detail(photographer_id):
    """摄影师主页：完整访问地址 /photographer/detail/<photographer_id>。

    展示摄影师资料和该摄影师公开可见的作品。
    """
    photographer = db.session.execute(
        select(Photographer)
        .options(joinedload(Photographer.user))
        .join(Photographer.user)
        .where(
            Photographer.photographer_id == photographer_id,
            Photographer.cert_status == Photographer.STATUS_APPROVED,
            User.status == 1,
        )
    ).scalar_one_or_none()
    if photographer is None:
        abort(404)

    works = db.session.execute(
        select(PhotoWork)
        .join(PhotoWork.photographer)
        .join(Photographer.user)
        .where(
            PhotoWork.photographer_id == photographer_id,
            PhotoWork.audit_status == PhotoWork.AUDIT_APPROVED,
            PhotoWork.status == 1,
            User.status == 1,
        )
        .order_by(PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
    ).scalars().all()
    return render_template('photographer/detail.html', photographer=photographer, works=works)


@admin_bp.route('/list')
@admin_required
def admin_list():
    """后台摄影师审核列表：完整访问地址 /admin/photographer/list。"""
    page = request.args.get('page', default=1, type=int)
    status = request.args.get('status', type=int)
    stmt = (
        select(Photographer)
        .options(joinedload(Photographer.user))
        .order_by(Photographer.create_time.desc(), Photographer.photographer_id.desc())
    )
    if status in (0, 1, 2):
        stmt = stmt.where(Photographer.cert_status == status)
    photographers = db.paginate(stmt, page=page, per_page=10, error_out=False)
    return render_template('photographer/admin_list.html', photographers=photographers)


@admin_bp.route('/audit/<int:photographer_id>', methods=['GET', 'POST'])
@admin_required
def admin_audit(photographer_id):
    """后台摄影师审核。

    GET：打开审核页面。
    POST：保存审核通过/拒绝、审核备注、审核管理员和审核时间。
    """
    photographer = db.session.execute(
        select(Photographer)
        .options(joinedload(Photographer.user))
        .where(Photographer.photographer_id == photographer_id)
    ).scalar_one_or_none()
    if photographer is None:
        flash('摄影师认证记录不存在。', 'error')
        return redirect(url_for('admin_photographer.admin_list'))

    if request.method == 'POST':
        cert_status = request.form.get('cert_status', type=int)
        if cert_status not in (Photographer.STATUS_APPROVED, Photographer.STATUS_REJECTED):
            flash('审核状态无效。', 'error')
            return render_template('photographer/admin_audit.html', photographer=photographer)

        photographer.cert_status = cert_status
        photographer.cert_remark = request.form.get('cert_remark', '').strip() or None
        photographer.audit_admin_id = current_user.admin_id
        photographer.audit_time = datetime.now()
        if photographer.user:
            photographer.user.user_role = 2 if cert_status == Photographer.STATUS_APPROVED else photographer.user.user_role
        db.session.commit()
        log_admin_action('摄影师审核', f'审核摄影师：{photographer.user.username if photographer.user else photographer.photographer_id}')
        flash('摄影师审核已保存。', 'success')
        return redirect(url_for('admin_photographer.admin_list'))

    return render_template('photographer/admin_audit.html', photographer=photographer)
