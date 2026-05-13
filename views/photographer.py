from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from db import db
from models import PhotoWork, Photographer
from utils.decorators import admin_required
from utils.logger import log_admin_action


bp = Blueprint('photographer', __name__, url_prefix='/photographer')
admin_bp = Blueprint('admin_photographer', __name__, url_prefix='/admin/photographer')


@bp.route('/list')
def list_page():
    page = request.args.get('page', default=1, type=int)
    city = request.args.get('city', '').strip()
    stmt = (
        select(Photographer)
        .options(joinedload(Photographer.user), selectinload(Photographer.works))
        .where(Photographer.cert_status == Photographer.STATUS_APPROVED)
        .order_by(Photographer.create_time.desc(), Photographer.photographer_id.desc())
    )
    if city:
        stmt = stmt.where(Photographer.city.like(f'%{city}%'))
    photographers = db.paginate(stmt, page=page, per_page=9, error_out=False)
    return render_template('photographer/list.html', photographers=photographers)


@bp.route('/detail/<int:photographer_id>')
def detail(photographer_id):
    photographer = db.session.execute(
        select(Photographer)
        .options(joinedload(Photographer.user))
        .where(
            Photographer.photographer_id == photographer_id,
            Photographer.cert_status == Photographer.STATUS_APPROVED,
        )
    ).scalar_one_or_none()
    if photographer is None:
        abort(404)

    works = db.session.execute(
        select(PhotoWork)
        .where(
            PhotoWork.photographer_id == photographer_id,
            PhotoWork.audit_status == PhotoWork.AUDIT_APPROVED,
            PhotoWork.status == 1,
        )
        .order_by(PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
    ).scalars().all()
    return render_template('photographer/detail.html', photographer=photographer, works=works)


@admin_bp.route('/list')
@admin_required
def admin_list():
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
