from flask import Blueprint, render_template

from utils.demo_data import Pagination, categories


bp = Blueprint('category', __name__, url_prefix='/admin/category')


@bp.route('/list')
def list_page():
    return render_template('category/list.html', categories=Pagination(categories))


@bp.route('/add', methods=['GET', 'POST'])
@bp.route('/edit/<int:category_id>', methods=['GET', 'POST'])
def form(category_id=None):
    category = next((item for item in categories if item.category_id == category_id), None)
    return render_template('category/form.html', category=category)
