from flask import Flask, render_template
from flask_login import LoginManager
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from config import Config
from db import db
from models import Carousel, PhotoWork, Photographer
import models  # noqa: F401
from views.announcement import admin_bp as admin_announcement_bp
from views.announcement import bp as announcement_bp
from views.api import bp as api_bp
from views.auth import bp as auth_bp, load_user
from views.carousel import bp as carousel_bp
from views.category import bp as category_bp
from views.dashboard import bp as dashboard_bp
from views.forum import admin_bp as admin_forum_bp
from views.forum import bp as forum_bp
from views.photographer import admin_bp as admin_photographer_bp
from views.photographer import bp as photographer_bp
from views.user import admin_bp as admin_user_bp
from views.user import bp as user_bp
from views.work import admin_bp as admin_work_bp
from views.work import bp as work_bp


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def user_loader(user_id):
    return load_user(user_id)


app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(work_bp)
app.register_blueprint(admin_work_bp)
app.register_blueprint(photographer_bp)
app.register_blueprint(admin_photographer_bp)
app.register_blueprint(forum_bp)
app.register_blueprint(admin_forum_bp)
app.register_blueprint(announcement_bp)
app.register_blueprint(admin_announcement_bp)
app.register_blueprint(category_bp)
app.register_blueprint(carousel_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_user_bp)
app.register_blueprint(api_bp)


@app.route('/')
def index():
    work_user_load = joinedload(PhotoWork.photographer).joinedload(Photographer.user)

    carousels = db.session.execute(
        select(Carousel)
        .where(Carousel.status == 1)
        .order_by(Carousel.sort.asc(), Carousel.carousel_id.desc())
    ).scalars().all()

    featured_works = db.session.execute(
        select(PhotoWork)
        .options(work_user_load)
        .where(
            PhotoWork.audit_status == PhotoWork.AUDIT_APPROVED,
            PhotoWork.status == 1,
            PhotoWork.is_featured == 1,
        )
        .order_by(PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
        .limit(3)
    ).scalars().all()

    hot_works = db.session.execute(
        select(PhotoWork)
        .options(work_user_load)
        .where(
            PhotoWork.audit_status == PhotoWork.AUDIT_APPROVED,
            PhotoWork.status == 1,
        )
        .order_by(PhotoWork.hot_score.desc(), PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
        .limit(8)
    ).scalars().all()

    recent_works = db.session.execute(
        select(PhotoWork)
        .options(work_user_load)
        .where(
            PhotoWork.audit_status == PhotoWork.AUDIT_APPROVED,
            PhotoWork.status == 1,
        )
        .order_by(PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
        .limit(8)
    ).scalars().all()

    photographers = db.session.execute(
        select(Photographer)
        .options(joinedload(Photographer.user))
        .where(Photographer.cert_status == Photographer.STATUS_APPROVED)
        .order_by(Photographer.create_time.desc(), Photographer.photographer_id.desc())
        .limit(6)
    ).scalars().all()

    return render_template(
        'index.html',
        carousels=carousels,
        featured_works=featured_works,
        hot_works=hot_works,
        recent_works=recent_works,
        photographers=photographers,
    )


if __name__ == '__main__':
    app.run(debug=True)
