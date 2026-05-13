from flask import Blueprint, jsonify, request
from flask_login import current_user
from sqlalchemy import func, select

from db import db
from models import PhotoWork, WorkComment, WorkLike


bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/work/<int:work_id>/like', methods=['POST'])
def like_work(work_id):
    if not current_user.is_authenticated or getattr(current_user, 'is_admin', False):
        return jsonify({'success': False, 'message': '请先使用用户账号登录。'}), 401

    work = db.session.execute(
        select(PhotoWork).where(
            PhotoWork.work_id == work_id,
            PhotoWork.audit_status == PhotoWork.AUDIT_APPROVED,
            PhotoWork.status == 1,
        )
    ).scalar_one_or_none()
    if work is None:
        return jsonify({'success': False, 'message': '作品不存在。'}), 404

    like = db.session.execute(
        select(WorkLike).where(
            WorkLike.work_id == work_id,
            WorkLike.user_id == current_user.user_id,
        )
    ).scalar_one_or_none()

    if like is None:
        db.session.add(WorkLike(work_id=work_id, user_id=current_user.user_id))
        liked = True
    else:
        db.session.delete(like)
        liked = False

    db.session.flush()
    work.like_count = db.session.execute(
        select(func.count(WorkLike.like_id)).where(WorkLike.work_id == work_id)
    ).scalar_one()
    work.update_hot_score()
    db.session.commit()

    return jsonify({'success': True, 'liked': liked, 'count': work.like_count})


@bp.route('/work/<int:work_id>/comment', methods=['POST'])
def add_comment(work_id):
    if not current_user.is_authenticated or getattr(current_user, 'is_admin', False):
        return jsonify({'success': False, 'message': '请先使用用户账号登录。'}), 401

    work = db.session.execute(
        select(PhotoWork).where(
            PhotoWork.work_id == work_id,
            PhotoWork.audit_status == PhotoWork.AUDIT_APPROVED,
            PhotoWork.status == 1,
        )
    ).scalar_one_or_none()
    if work is None:
        return jsonify({'success': False, 'message': '作品不存在。'}), 404

    content = request.form.get('content', '').strip()
    if not content:
        return jsonify({'success': False, 'message': '评论内容不能为空。'}), 400

    db.session.add(
        WorkComment(
            work_id=work_id,
            user_id=current_user.user_id,
            content=content,
            audit_status=1,
            status=1,
        )
    )
    db.session.flush()
    work.comment_count = db.session.execute(
        select(func.count(WorkComment.comment_id)).where(
            WorkComment.work_id == work_id,
            WorkComment.status == 1,
            WorkComment.audit_status == 1,
        )
    ).scalar_one()
    work.update_hot_score()
    db.session.commit()

    return jsonify({'success': True})
