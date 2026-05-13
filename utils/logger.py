from flask import request
from flask_login import current_user

from db import db
from models import SystemLog


def log_admin_action(operate_type: str, operate_content: str) -> None:
    if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
        return

    log = SystemLog(
        admin_id=current_user.admin_id,
        operate_type=operate_type[:30],
        operate_content=operate_content[:255],
        ip_address=(request.headers.get('X-Forwarded-For') or request.remote_addr or '')[:50],
    )
    try:
        db.session.add(log)
        db.session.commit()
    except Exception:
        db.session.rollback()
