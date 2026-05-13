from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import select

from db import db
from models import Carousel
from utils.decorators import admin_required
from utils.file_upload import save_image


bp = Blueprint('carousel', __name__, url_prefix='/admin/carousel')


@bp.route('/list')
@admin_required
def list_page():
    carousels = db.session.execute(
        select(Carousel).order_by(Carousel.sort.asc(), Carousel.carousel_id.desc())
    ).scalars().all()
    return render_template('carousel/list.html', carousels=carousels)


@bp.route('/add', methods=['GET', 'POST'])
@bp.route('/edit/<int:carousel_id>', methods=['GET', 'POST'])
@admin_required
def form(carousel_id=None):
    carousel = db.session.get(Carousel, carousel_id) if carousel_id else Carousel(status=1)
    if carousel is None:
        flash('轮播图不存在。', 'error')
        return redirect(url_for('carousel.list_page'))

    if request.method == 'POST':
        carousel.title = request.form.get('title', '').strip() or None
        carousel.image_url = request.form.get('image_url', '').strip()
        carousel.link_type = request.form.get('link_type', '').strip() or None
        carousel.link_id = request.form.get('link_id', type=int)
        carousel.link_url = request.form.get('link_url', '').strip() or None
        carousel.sort = request.form.get('sort', type=int, default=0)

        try:
            image_url = save_image(request.files.get('image_file'), 'carousels')
            if image_url:
                carousel.image_url = image_url
        except ValueError as exc:
            flash(str(exc), 'error')
            return render_template('carousel/form.html', carousel=carousel)

        if not carousel.image_url:
            flash('图片 URL 或上传图片不能为空。', 'error')
            return render_template('carousel/form.html', carousel=carousel)

        db.session.add(carousel)
        db.session.commit()
        flash('轮播图已保存。', 'success')
        return redirect(url_for('carousel.list_page'))

    return render_template('carousel/form.html', carousel=carousel if carousel_id else None)


@bp.route('/status/<int:carousel_id>')
@admin_required
def toggle_status(carousel_id):
    carousel = db.session.get(Carousel, carousel_id)
    if carousel is None:
        flash('轮播图不存在。', 'error')
    else:
        carousel.status = 0 if carousel.status == 1 else 1
        db.session.commit()
        flash('轮播图状态已更新。', 'success')
    return redirect(url_for('carousel.list_page'))


@bp.route('/delete/<int:carousel_id>')
@admin_required
def delete(carousel_id):
    carousel = db.session.get(Carousel, carousel_id)
    if carousel is not None:
        db.session.delete(carousel)
        db.session.commit()
        flash('轮播图已删除。', 'success')
    return redirect(url_for('carousel.list_page'))
