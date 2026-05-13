from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from db import db
from models import Category
from utils.decorators import admin_required
from utils.logger import log_admin_action


bp = Blueprint('category', __name__, url_prefix='/admin/category')


@bp.route('/list')
@admin_required
def list_page():
    page = request.args.get('page', default=1, type=int)
    category_name = request.args.get('category_name', '').strip()
    stmt = select(Category).order_by(Category.sort.asc(), Category.category_id.asc())
    if category_name:
        stmt = stmt.where(Category.category_name.like(f'%{category_name}%'))
    categories = db.paginate(stmt, page=page, per_page=10, error_out=False)
    return render_template('category/list.html', categories=categories)


@bp.route('/add', methods=['GET', 'POST'])
@bp.route('/edit/<int:category_id>', methods=['GET', 'POST'])
@admin_required
def form(category_id=None):
    category = db.session.get(Category, category_id) if category_id else Category(status=1)
    if category is None:
        flash('分类不存在。', 'error')
        return redirect(url_for('category.list_page'))

    if request.method == 'POST':
        category.category_name = request.form.get('category_name', '').strip()
        category.sort = request.form.get('sort', type=int, default=0)

        if not category.category_name:
            flash('分类名称不能为空。', 'error')
            return render_template('category/form.html', category=category)

        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('分类名称已存在。', 'error')
            return render_template('category/form.html', category=category)

        flash('分类已保存。', 'success')
        log_admin_action('分类保存', f'保存分类：{category.category_name}')
        return redirect(url_for('category.list_page'))

    return render_template('category/form.html', category=category if category_id else None)


@bp.route('/status/<int:category_id>', methods=['POST'])
@admin_required
def toggle_status(category_id):
    category = db.session.get(Category, category_id)
    if category is None:
        flash('分类不存在。', 'error')
    else:
        category.status = 0 if category.status == 1 else 1
        db.session.commit()
        log_admin_action('分类状态', f'更新分类状态：{category.category_name}')
        flash('分类状态已更新。', 'success')
    return redirect(url_for('category.list_page'))
