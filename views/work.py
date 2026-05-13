from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from db import db
from models import Category, PhotoWork, PhotoWorkImage, Photographer, WorkComment, WorkLike
from utils.decorators import admin_required
from utils.file_upload import save_image


bp = Blueprint('work', __name__, url_prefix='/work')
admin_bp = Blueprint('admin_work', __name__, url_prefix='/admin/work')


@bp.route('/list')
def list_page():
    page = request.args.get('page', default=1, type=int)
    keyword = request.args.get('keyword', '').strip()
    category_id = request.args.get('category_id', type=int)
    city = request.args.get('city', '').strip()
    sort_by = request.args.get('sort_by', 'hot').strip().lower()

    categories = db.session.execute(
        select(Category)
        .where(Category.status == 1)
        .order_by(Category.sort.asc(), Category.category_id.asc())
    ).scalars().all()

    stmt = (
        select(PhotoWork)
        .options(
            joinedload(PhotoWork.category),
            joinedload(PhotoWork.photographer).joinedload(Photographer.user),
        )
        .where(
            PhotoWork.audit_status == PhotoWork.AUDIT_APPROVED,
            PhotoWork.status == 1,
        )
    )

    if keyword:
        stmt = stmt.where(PhotoWork.title.like(f'%{keyword}%'))
    if category_id:
        stmt = stmt.where(PhotoWork.category_id == category_id)
    if city:
        stmt = stmt.where(PhotoWork.city.like(f'%{city}%'))

    if sort_by == 'new':
        stmt = stmt.order_by(PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
    else:
        stmt = stmt.order_by(PhotoWork.hot_score.desc(), PhotoWork.create_time.desc(), PhotoWork.work_id.desc())

    works = db.paginate(stmt, page=page, per_page=9, error_out=False)
    return render_template('work/list.html', works=works, categories=categories)


@bp.route('/detail/<int:work_id>')
def detail(work_id):
    work = db.session.execute(
        select(PhotoWork)
        .options(
            joinedload(PhotoWork.category),
            joinedload(PhotoWork.photographer).joinedload(Photographer.user),
            selectinload(PhotoWork.images),
        )
        .where(
            PhotoWork.work_id == work_id,
            PhotoWork.audit_status == PhotoWork.AUDIT_APPROVED,
            PhotoWork.status == 1,
        )
    ).scalar_one_or_none()

    if work is None:
        abort(404)

    work.view_count = (work.view_count or 0) + 1
    work.update_hot_score()
    db.session.commit()

    comments = db.session.execute(
        select(WorkComment)
        .options(joinedload(WorkComment.user))
        .where(
            WorkComment.work_id == work_id,
            WorkComment.status == 1,
            WorkComment.audit_status == 1,
        )
        .order_by(WorkComment.create_time.asc(), WorkComment.comment_id.asc())
    ).scalars().all()

    is_liked = False
    if current_user.is_authenticated and not getattr(current_user, 'is_admin', False):
        is_liked = db.session.execute(
            select(WorkLike).where(
                WorkLike.work_id == work_id,
                WorkLike.user_id == current_user.user_id,
            )
        ).scalar_one_or_none() is not None

    return render_template('work/detail.html', work=work, comments=comments, is_liked=is_liked)


@admin_bp.route('/list')
@admin_required
def admin_list():
    page = request.args.get('page', default=1, type=int)
    title = request.args.get('title', '').strip()
    audit_status = request.args.get('audit_status', type=int)
    status = request.args.get('status', type=int)

    stmt = (
        select(PhotoWork)
        .options(
            joinedload(PhotoWork.category),
            joinedload(PhotoWork.photographer).joinedload(Photographer.user),
        )
        .order_by(PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
    )
    if title:
        stmt = stmt.where(PhotoWork.title.like(f'%{title}%'))
    if audit_status in (0, 1, 2):
        stmt = stmt.where(PhotoWork.audit_status == audit_status)
    if status in (0, 1):
        stmt = stmt.where(PhotoWork.status == status)

    works = db.paginate(stmt, page=page, per_page=10, error_out=False)
    return render_template('work/admin_list.html', works=works)


@admin_bp.route('/add', methods=['GET', 'POST'])
@admin_bp.route('/edit/<int:work_id>', methods=['GET', 'POST'])
@admin_required
def admin_form(work_id=None):
    work = db.session.get(PhotoWork, work_id) if work_id else PhotoWork(status=1, audit_status=PhotoWork.AUDIT_APPROVED)
    if work is None:
        flash('作品不存在。', 'error')
        return redirect(url_for('admin_work.admin_list'))

    photographers = db.session.execute(
        select(Photographer)
        .options(joinedload(Photographer.user))
        .where(Photographer.cert_status == Photographer.STATUS_APPROVED)
        .order_by(Photographer.photographer_id.desc())
    ).scalars().all()
    categories = db.session.execute(
        select(Category).where(Category.status == 1).order_by(Category.sort.asc(), Category.category_id.asc())
    ).scalars().all()

    if request.method == 'POST':
        work.title = request.form.get('title', '').strip()
        work.photographer_id = request.form.get('photographer_id', type=int)
        work.category_id = request.form.get('category_id', type=int)
        work.city = request.form.get('city', '').strip() or None
        work.description = request.form.get('description', '').strip() or None

        if not work.title or not work.photographer_id or not work.category_id:
            flash('标题、摄影师和分类不能为空。', 'error')
            return render_template('work/admin_form.html', work=work, photographers=photographers, categories=categories)

        try:
            cover_url = save_image(request.files.get('cover_file'), 'works')
            if cover_url:
                work.cover_url = cover_url
        except ValueError as exc:
            flash(str(exc), 'error')
            return render_template('work/admin_form.html', work=work, photographers=photographers, categories=categories)

        db.session.add(work)
        db.session.flush()

        for sort, image_file in enumerate(request.files.getlist('work_images'), start=1):
            try:
                image_url = save_image(image_file, 'works')
            except ValueError as exc:
                db.session.rollback()
                flash(str(exc), 'error')
                return render_template('work/admin_form.html', work=work, photographers=photographers, categories=categories)
            if image_url:
                db.session.add(PhotoWorkImage(work_id=work.work_id, image_url=image_url, sort=sort))

        work.update_hot_score()
        db.session.commit()
        flash('作品已保存。', 'success')
        return redirect(url_for('admin_work.admin_list'))

    return render_template(
        'work/admin_form.html',
        work=work if work_id else None,
        photographers=photographers,
        categories=categories,
    )


@admin_bp.route('/<int:work_id>/audit', methods=['POST'])
@admin_required
def audit(work_id):
    work = db.session.get(PhotoWork, work_id)
    if work is None:
        return jsonify({'success': False, 'message': '作品不存在。'}), 404
    audit_status = request.form.get('audit_status', type=int)
    if audit_status not in (PhotoWork.AUDIT_APPROVED, PhotoWork.AUDIT_REJECTED):
        return jsonify({'success': False, 'message': '审核状态无效。'}), 400
    work.audit_status = audit_status
    db.session.commit()
    return jsonify({'success': True})


@admin_bp.route('/delete/<int:work_id>')
@admin_required
def delete(work_id):
    work = db.session.get(PhotoWork, work_id)
    if work is not None:
        work.status = 0
        db.session.commit()
        flash('作品已下架。', 'success')
    return redirect(url_for('admin_work.admin_list'))
