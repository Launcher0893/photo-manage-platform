from flask import Blueprint, render_template
from sqlalchemy import func, select

from db import db
from models import Category, PhotoWork, Photographer, User
from utils.decorators import admin_required


bp = Blueprint('dashboard', __name__, url_prefix='/admin/dashboard')


@bp.route('/')
@bp.route('/index')
@admin_required
def index():
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
    )
