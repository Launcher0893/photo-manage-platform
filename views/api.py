"""JSON API 接口模块。

蓝图前缀：/api

本文件中的路由通常不直接返回 HTML 页面，而是返回 JSON。
主要用于：
- 作品点赞。
- 作品评论。
- 后台控制台图表数据。
"""

from datetime import date, datetime, timedelta

from flask import Blueprint, jsonify, request
from flask_login import current_user
from sqlalchemy import func, select

from db import db
from models import Category, ForumComment, ForumPost, PhotoWork, User, WorkComment, WorkLike
from utils.decorators import admin_required


bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/work/<int:work_id>/like', methods=['POST'])
def like_work(work_id):
    """作品点赞/取消点赞接口。

    POST /api/work/<work_id>/like
    前端 Ajax 调用，返回 JSON：是否成功、是否已点赞、最新点赞数。
    """
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
    """作品评论接口。

    POST /api/work/<work_id>/comment
    保存评论后重新统计作品评论数，并更新热度。
    """
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


@bp.route('/dashboard/trends')
@admin_required
def dashboard_trends():
    """后台趋势图接口：返回最近 7 天用户数和作品数。"""
    today = date.today()
    days = [today - timedelta(days=offset) for offset in range(6, -1, -1)]
    start_dt = datetime.combine(days[0], datetime.min.time())

    user_rows = db.session.execute(
        select(func.date(User.create_time), func.count(User.user_id))
        .where(User.create_time >= start_dt)
        .group_by(func.date(User.create_time))
    ).all()
    work_rows = db.session.execute(
        select(func.date(PhotoWork.create_time), func.count(PhotoWork.work_id))
        .where(PhotoWork.create_time >= start_dt)
        .group_by(func.date(PhotoWork.create_time))
    ).all()

    user_map = {str(day): count for day, count in user_rows}
    work_map = {str(day): count for day, count in work_rows}
    labels = [day.strftime('%m-%d') for day in days]
    keys = [day.isoformat() for day in days]
    return jsonify({
        'labels': labels,
        'users': [user_map.get(key, 0) for key in keys],
        'works': [work_map.get(key, 0) for key in keys],
    })


@bp.route('/dashboard/forum_activity')
@admin_required
def dashboard_forum_activity():
    """后台论坛活跃图接口：返回最近 7 天帖子数和评论数。"""
    today = date.today()
    days = [today - timedelta(days=offset) for offset in range(6, -1, -1)]
    start_dt = datetime.combine(days[0], datetime.min.time())

    post_rows = db.session.execute(
        select(func.date(ForumPost.create_time), func.count(ForumPost.post_id))
        .where(ForumPost.create_time >= start_dt)
        .group_by(func.date(ForumPost.create_time))
    ).all()
    comment_rows = db.session.execute(
        select(func.date(ForumComment.create_time), func.count(ForumComment.comment_id))
        .where(ForumComment.create_time >= start_dt)
        .group_by(func.date(ForumComment.create_time))
    ).all()

    post_map = {str(day): count for day, count in post_rows}
    comment_map = {str(day): count for day, count in comment_rows}
    labels = [day.strftime('%m-%d') for day in days]
    keys = [day.isoformat() for day in days]
    return jsonify({
        'labels': labels,
        'posts': [post_map.get(key, 0) for key in keys],
        'comments': [comment_map.get(key, 0) for key in keys],
    })


@bp.route('/dashboard/category_stats')
@admin_required
def dashboard_category_stats():
    """后台分类统计接口：返回每个分类下的作品数量。"""
    rows = db.session.execute(
        select(Category.category_name, func.count(PhotoWork.work_id))
        .outerjoin(PhotoWork, PhotoWork.category_id == Category.category_id)
        .group_by(Category.category_id, Category.category_name)
        .order_by(Category.sort.asc(), Category.category_id.asc())
    ).all()
    return jsonify([
        {'name': category_name, 'value': count}
        for category_name, count in rows
    ])
