from flask import Blueprint, render_template

from utils.demo_data import Pagination, get_photographer, photographers


bp = Blueprint('photographer', __name__, url_prefix='/photographer')
admin_bp = Blueprint('admin_photographer', __name__, url_prefix='/admin/photographer')


@bp.route('/list')
def list_page():
    return render_template('photographer/list.html', photographers=Pagination(photographers))


@bp.route('/detail/<int:photographer_id>')
def detail(photographer_id):
    photographer = get_photographer(photographer_id) or photographers[0]
    return render_template('photographer/detail.html', photographer=photographer, works=photographer.works)


@admin_bp.route('/list')
def admin_list():
    return render_template('photographer/admin_list.html', photographers=Pagination(photographers))


@admin_bp.route('/audit/<int:photographer_id>', methods=['GET', 'POST'])
def admin_audit(photographer_id):
    photographer = get_photographer(photographer_id) or photographers[0]
    return render_template('photographer/admin_audit.html', photographer=photographer)
