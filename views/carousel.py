"""后台轮播图管理模块。

蓝图前缀：/admin/carousel
首页轮播图的数据来自 carousel 表，后台在这里维护。
前台展示逻辑在 templates/index.html 的自定义轮播组件中。
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import select

from db import db
from models import Carousel
from utils.decorators import admin_required
from utils.file_upload import delete_uploaded_file, save_image
from utils.logger import log_admin_action


bp = Blueprint('carousel', __name__, url_prefix='/admin/carousel')


@bp.route('/list')
@admin_required
def list_page():
    """轮播图列表：完整访问地址 /admin/carousel/list。"""
    carousels = db.session.execute(
        select(Carousel).order_by(Carousel.sort.asc(), Carousel.carousel_id.desc())
    ).scalars().all()
    return render_template('carousel/list.html', carousels=carousels)


@bp.route('/add', methods=['GET', 'POST'])
@bp.route('/edit/<int:carousel_id>', methods=['GET', 'POST'])
@admin_required
def form(carousel_id=None):
    """新增/编辑轮播图。

    可以填写图片 URL，也可以上传图片。
    link_type/link_id/link_url 用于首页点击轮播图后跳转。
    """
    carousel = db.session.get(Carousel, carousel_id) if carousel_id else Carousel(status=1)
    if carousel is None:
        flash('轮播图不存在。', 'error')
        return redirect(url_for('carousel.list_page'))

    if request.method == 'POST':
        old_image_url = carousel.image_url
        should_delete_old_image = False
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
                should_delete_old_image = True
        except ValueError as exc:
            flash(str(exc), 'error')
            return render_template('carousel/form.html', carousel=carousel)

        if not carousel.image_url:
            flash('图片 URL 或上传图片不能为空。', 'error')
            return render_template('carousel/form.html', carousel=carousel)

        db.session.add(carousel)
        db.session.commit()
        if should_delete_old_image:
            delete_uploaded_file(old_image_url)
        log_admin_action('轮播图保存', f'保存轮播图：{carousel.title or carousel.carousel_id}')
        flash('轮播图已保存。', 'success')
        return redirect(url_for('carousel.list_page'))

    return render_template('carousel/form.html', carousel=carousel if carousel_id else None)


@bp.route('/status/<int:carousel_id>', methods=['POST'])
@admin_required
def toggle_status(carousel_id):
    """启用/停用轮播图。首页只显示 status=1 的轮播图。"""
    carousel = db.session.get(Carousel, carousel_id)
    if carousel is None:
        flash('轮播图不存在。', 'error')
    else:
        carousel.status = 0 if carousel.status == 1 else 1
        db.session.commit()
        log_admin_action('轮播图状态', f'更新轮播图状态：{carousel.title or carousel.carousel_id}')
        flash('轮播图状态已更新。', 'success')
    return redirect(url_for('carousel.list_page'))


@bp.route('/delete/<int:carousel_id>', methods=['POST'])
@admin_required
def delete(carousel_id):
    """删除轮播图记录，并尝试删除对应图片。"""
    carousel = db.session.get(Carousel, carousel_id)
    if carousel is not None:
        title = carousel.title or carousel_id
        delete_ok = delete_uploaded_file(carousel.image_url)
        db.session.delete(carousel)
        db.session.commit()
        if delete_ok:
            log_admin_action('轮播图删除', f'删除轮播图：{title}')
            flash('轮播图已删除。', 'success')
        else:
            flash('轮播图已删除，但图片文件删除失败。', 'error')
    return redirect(url_for('carousel.list_page'))
