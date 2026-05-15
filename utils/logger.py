"""后台操作日志工具。

管理员执行保存、审核、删除、状态切换等操作时，
业务代码调用 log_admin_action() 写入 system_log 表。
"""

from flask import request
from flask_login import current_user

from db import db
from models import SystemLog


def log_admin_action(operate_type: str, operate_content: str) -> None:
    """记录一条管理员操作日志。

    operate_type：操作类型，例如“作品状态”“公告保存”。
    operate_content：具体操作内容。

    这个函数内部自己 commit；如果写日志失败，只回滚日志，不影响主业务。
    """
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
