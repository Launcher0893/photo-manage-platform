from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import select

from db import db
from models import Announcement
from utils.decorators import admin_required
from utils.file_upload import delete_uploaded_file, save_image
from utils.logger import log_admin_action


bp = Blueprint('announcement', __name__, url_prefix='/announcement')
admin_bp = Blueprint('admin_announcement', __name__, url_prefix='/admin/announcement')


@bp.route('/list')
def list_page():
    page = request.args.get('page', default=1, type=int)
    stmt = (
        select(Announcement)
        .where(Announcement.status == 1)
        .order_by(Announcement.create_time.desc(), Announcement.announcement_id.desc())
    )
    announcements = db.paginate(stmt, page=page, per_page=10, error_out=False)
    return render_template('announcement/list.html', announcements=announcements)


@bp.route('/detail/<int:announcement_id>')
def detail(announcement_id):
    announcement = db.session.execute(
        select(Announcement).where(
            Announcement.announcement_id == announcement_id,
            Announcement.status == 1,
        )
    ).scalar_one_or_none()
    if announcement is None:
        abort(404)
    return render_template('announcement/detail.html', announcement=announcement)


@admin_bp.route('/list')
@admin_required
def admin_list():
    page = request.args.get('page', default=1, type=int)
    announcements = db.paginate(
        select(Announcement).order_by(Announcement.create_time.desc(), Announcement.announcement_id.desc()),
        page=page,
        per_page=10,
        error_out=False,
    )
    return render_template('announcement/admin_list.html', announcements=announcements)


@admin_bp.route('/add', methods=['GET', 'POST'])
@admin_bp.route('/edit/<int:announcement_id>', methods=['GET', 'POST'])
@admin_required
def admin_form(announcement_id=None):
    announcement = db.session.get(Announcement, announcement_id) if announcement_id else Announcement(status=1)
    if announcement is None:
        flash('公告不存在。', 'error')
        return redirect(url_for('admin_announcement.admin_list'))

    if request.method == 'POST':
        old_cover_url = None
        announcement.title = request.form.get('title', '').strip()
        announcement.content = request.form.get('content', '').strip()
        if not announcement.title or not announcement.content:
            flash('标题和内容不能为空。', 'error')
            return render_template('announcement/admin_form.html', announcement=announcement)

        try:
            cover_url = save_image(request.files.get('cover_file'), 'announcements')
            if cover_url:
                old_cover_url = announcement.cover_url
                announcement.cover_url = cover_url
        except ValueError as exc:
            flash(str(exc), 'error')
            return render_template('announcement/admin_form.html', announcement=announcement)

        if not announcement_id:
            announcement.admin_id = current_user.admin_id
        db.session.add(announcement)
        db.session.commit()
        delete_uploaded_file(old_cover_url)
        log_admin_action('公告保存', f'保存公告：{announcement.title}')
        flash('公告已保存。', 'success')
        return redirect(url_for('admin_announcement.admin_list'))

    return render_template('announcement/admin_form.html', announcement=announcement if announcement_id else None)


@admin_bp.route('/status/<int:announcement_id>')
@admin_required
def toggle_status(announcement_id):
    announcement = db.session.get(Announcement, announcement_id)
    if announcement is not None:
        announcement.status = 0 if announcement.status == 1 else 1
        db.session.commit()
        log_admin_action('公告状态', f'更新公告状态：{announcement.title}')
        flash('公告状态已更新。', 'success')
    return redirect(url_for('admin_announcement.admin_list'))


@admin_bp.route('/delete/<int:announcement_id>')
@admin_required
def delete(announcement_id):
    announcement = db.session.get(Announcement, announcement_id)
    if announcement is None:
        flash('公告不存在。', 'error')
        return redirect(url_for('admin_announcement.admin_list'))

    title = announcement.title
    cover_url = announcement.cover_url
    db.session.delete(announcement)
    db.session.commit()
    delete_ok = delete_uploaded_file(cover_url)
    log_admin_action('公告删除', f'删除公告：{title}')
    if delete_ok:
        flash('公告已删除。', 'success')
    else:
        flash('公告已删除，但封面图片删除失败。', 'error')
    return redirect(url_for('admin_announcement.admin_list'))
