from flask import Blueprint, render_template

from utils.demo_data import Pagination, photographers, works


bp = Blueprint('dashboard', __name__, url_prefix='/admin/dashboard')


@bp.route('/')
@bp.route('/index')
def index():
    return render_template(
        'dashboard/index.html',
        total_works=len(works),
        total_users=2,
        approved_photographers=sum(1 for item in photographers if item.cert_status == 1),
        pending_photographers=sum(1 for item in photographers if item.cert_status == 0),
        hot_works=sorted(works, key=lambda item: item.hot_score, reverse=True)[:10],
        page_data=Pagination([])
    )
