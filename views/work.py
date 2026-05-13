from flask import Blueprint, render_template

from utils.demo_data import Pagination, categories, comments, get_work, photographers, works


bp = Blueprint('work', __name__, url_prefix='/work')
admin_bp = Blueprint('admin_work', __name__, url_prefix='/admin/work')


@bp.route('/list')
def list_page():
    return render_template('work/list.html', works=Pagination(works), categories=categories)


@bp.route('/detail/<int:work_id>')
def detail(work_id):
    work = get_work(work_id) or works[0]
    return render_template('work/detail.html', work=work, comments=comments, is_liked=False)


@admin_bp.route('/list')
def admin_list():
    return render_template('work/admin_list.html', works=Pagination(works))


@admin_bp.route('/add', methods=['GET', 'POST'])
@admin_bp.route('/edit/<int:work_id>', methods=['GET', 'POST'])
def admin_form(work_id=None):
    work = get_work(work_id) if work_id else None
    return render_template('work/admin_form.html', work=work, photographers=photographers, categories=categories)
