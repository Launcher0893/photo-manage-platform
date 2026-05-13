from flask import Blueprint, render_template, request
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db import db
from models import SystemLog
from utils.decorators import admin_required


bp = Blueprint('system', __name__, url_prefix='/admin/system')


@bp.route('/logs')
@admin_required
def log_list():
    page = request.args.get('page', default=1, type=int)
    operate_type = request.args.get('operate_type', '').strip()

    stmt = (
        select(SystemLog)
        .options(joinedload(SystemLog.admin))
        .order_by(SystemLog.operate_time.desc(), SystemLog.log_id.desc())
    )
    if operate_type:
        stmt = stmt.where(SystemLog.operate_type.like(f'%{operate_type}%'))

    logs = db.paginate(stmt, page=page, per_page=15, error_out=False)
    return render_template('system/log_list.html', logs=logs)
