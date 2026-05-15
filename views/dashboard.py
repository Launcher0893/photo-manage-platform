"""管理员后台控制台模块。

蓝图前缀：/admin/dashboard
主要页面：
- /admin/dashboard/
- /admin/dashboard/index

控制台展示平台统计数据、热门作品、待审核摄影师、最新用户、热门帖子等。
"""

from flask import Blueprint, render_template
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from db import db
from models import Category, ForumPost, PhotoWork, Photographer, User
from utils.decorators import admin_required


bp = Blueprint('dashboard', __name__, url_prefix='/admin/dashboard')


@bp.route('/')
@bp.route('/index')
@admin_required
def index():
    """后台控制台首页。

    这里主要做聚合查询，例如 count() 统计数量、order_by() 排序取热门/最新数据。
    最后渲染 templates/dashboard/index.html。
    """
    total_works = db.session.scalar(select(func.count(PhotoWork.work_id))) or 0
    total_users = db.session.scalar(select(func.count(User.user_id))) or 0
    approved_photographers = db.session.scalar(
        select(func.count(Photographer.photographer_id)).where(
            Photographer.cert_status == Photographer.STATUS_APPROVED
        )
    ) or 0
    pending_photographers = db.session.scalar(
        select(func.count(Photographer.photographer_id)).where(
            Photographer.cert_status == Photographer.STATUS_PENDING
        )
    ) or 0

    hot_works = db.session.execute(
        select(PhotoWork)
        .where(PhotoWork.status == 1)
        .order_by(PhotoWork.hot_score.desc(), PhotoWork.work_id.desc())
        .limit(10)
    ).scalars().all()

    pending_photographer_list = db.session.execute(
        select(Photographer)
        .options(joinedload(Photographer.user))
        .where(Photographer.cert_status == Photographer.STATUS_PENDING)
        .order_by(Photographer.create_time.desc(), Photographer.photographer_id.desc())
        .limit(5)
    ).scalars().all()

    latest_users = db.session.execute(
        select(User)
        .order_by(User.create_time.desc(), User.user_id.desc())
        .limit(5)
    ).scalars().all()

    latest_works = db.session.execute(
        select(PhotoWork)
        .options(
            joinedload(PhotoWork.category),
            joinedload(PhotoWork.photographer).joinedload(Photographer.user),
        )
        .order_by(PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
        .limit(5)
    ).scalars().all()

    post_hot_score = (
        func.coalesce(ForumPost.view_count, 0)
        + func.coalesce(ForumPost.like_count, 0) * 3
        + func.coalesce(ForumPost.comment_count, 0) * 2
    )
    hot_posts = db.session.execute(
        select(ForumPost)
        .options(joinedload(ForumPost.user), joinedload(ForumPost.forum_board))
        .where(ForumPost.status == 1)
        .order_by(post_hot_score.desc(), ForumPost.create_time.desc(), ForumPost.post_id.desc())
        .limit(5)
    ).scalars().all()

    category_stats = db.session.execute(
        select(Category.category_name, func.count(PhotoWork.work_id))
        .outerjoin(PhotoWork, PhotoWork.category_id == Category.category_id)
        .group_by(Category.category_id, Category.category_name)
        .order_by(Category.sort.asc(), Category.category_id.asc())
    ).all()

    return render_template(
        'dashboard/index.html',
        total_works=total_works,
        total_users=total_users,
        approved_photographers=approved_photographers,
        pending_photographers=pending_photographers,
        hot_works=hot_works,
        category_stats=category_stats,
        pending_photographer_list=pending_photographer_list,
        latest_users=latest_users,
        latest_works=latest_works,
        hot_posts=hot_posts,
    )
