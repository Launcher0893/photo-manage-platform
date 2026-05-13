from flask import Blueprint, render_template

from utils.demo_data import Pagination, announcements, get_announcement


bp = Blueprint('announcement', __name__, url_prefix='/announcement')
admin_bp = Blueprint('admin_announcement', __name__, url_prefix='/admin/announcement')


@bp.route('/list')
def list_page():
    return render_template('announcement/list.html', announcements=Pagination(announcements))


@bp.route('/detail/<int:announcement_id>')
def detail(announcement_id):
    announcement = get_announcement(announcement_id) or announcements[0]
    return render_template('announcement/detail.html', announcement=announcement)


@admin_bp.route('/list')
def admin_list():
    return render_template('announcement/admin_list.html', announcements=Pagination(announcements))


@admin_bp.route('/add', methods=['GET', 'POST'])
@admin_bp.route('/edit/<int:announcement_id>', methods=['GET', 'POST'])
def admin_form(announcement_id=None):
    announcement = get_announcement(announcement_id) if announcement_id else None
    return render_template('announcement/admin_form.html', announcement=announcement)
