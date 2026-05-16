"""项目入口文件。

这个文件可以理解成整个 Flask 项目的“总开关”：
1. 创建 Flask 应用对象 app。
2. 读取 config.py 中的配置。
3. 初始化数据库、登录管理和 CSRF 防护。
4. 注册 views/ 目录下各个功能模块的蓝图。
5. 定义首页 / 和 photo/ 静态图片访问。

具体业务逻辑大多不写在 app.py，而是拆到 views/*.py 中。
"""

from flask import Flask, jsonify, redirect, render_template, request, send_from_directory, url_for
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFError, CSRFProtect
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload
import os

from config import Config
from db import db
from models import Announcement, Carousel, PhotoWork, Photographer, User
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
from views.system import bp as system_bp
from views.user import admin_bp as admin_user_bp
from views.user import bp as user_bp
from views.work import admin_bp as admin_work_bp
from views.work import bp as work_bp


# 创建 Flask 应用对象。__name__ 用来让 Flask 找到当前项目路径和 templates/static 目录。
app = Flask(__name__)

# 从 config.py 的 Config 类读取数据库、密钥、OSS 等配置。
app.config.from_object(Config)

# 把 SQLAlchemy 数据库对象绑定到当前 Flask 应用。
db.init_app(app)

# 开启 CSRF 防护：所有 POST 表单都需要带 csrf_token，Ajax 需要带 X-CSRFToken。
csrf = CSRFProtect()
csrf.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
# 未登录用户访问受保护页面时，Flask-Login 会跳转到 auth.login，也就是 /auth/login。
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def user_loader(user_id):
    """Flask-Login 回调函数：根据 session 中保存的 id 重新加载当前用户。

    真实加载逻辑在 views/auth.py 的 load_user() 中。
    普通用户 id 形如 user:1，管理员 id 形如 admin:1。
    """
    return load_user(user_id)


@app.errorhandler(CSRFError)
def handle_csrf_error(error):
    """统一处理 CSRF 校验失败。

    普通表单返回一段错误文字；如果是 Ajax/JSON 请求，则返回 JSON 和 400 状态码。
    """
    message = 'CSRF 校验失败，请刷新页面后重试。'
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accept_mimetypes.best == 'application/json':
        return jsonify({'success': False, 'message': message}), 400
    return message, 400


# 注册蓝图：把 views/*.py 中定义的路由真正挂到 app 上。
# 例如 work_bp 的 url_prefix 是 /work，里面的 @bp.route('/list') 注册后就是 /work/list。
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
app.register_blueprint(system_bp)


@app.route('/photo/<path:filename>')
def photo_static(filename):
    """访问 photo/ 目录下的演示图片。

    HTML 中写 <img src="/photo/logo.png"> 时，会进入这个函数，
    然后从项目根目录的 photo 文件夹中返回 logo.png。
    """
    photo_dir = os.path.join(app.root_path, 'photo')
    return send_from_directory(photo_dir, filename)


@app.route('/')
def index():
    """首页路由：完整访问地址是 /。

    这个函数负责查询首页需要展示的数据：
    轮播图、精选作品、热门作品、最新作品、推荐摄影师、最新公告等。
    最后通过 render_template('index.html', ...) 把数据传给 templates/index.html。
    """
    if current_user.is_authenticated and getattr(current_user, 'is_admin', False):
        # 管理员访问前台首页时直接进入后台控制台。
        return redirect(url_for('dashboard.index'))

    # joinedload 表示“查作品时顺便把关联的摄影师和用户也加载出来”，减少模板里再次查数据库。
    work_user_load = joinedload(PhotoWork.photographer).joinedload(Photographer.user)
    work_images_load = joinedload(PhotoWork.images)

    # 查询启用的轮播图，传给 index.html 中的自定义轮播组件。
    carousels = db.session.execute(
        select(Carousel)
        .where(Carousel.status == 1)
        .order_by(Carousel.sort.asc(), Carousel.carousel_id.desc())
    ).scalars().all()

    # 首页精选作品：审核通过、上架、被管理员设为精选，并且摄影师账号正常。
    featured_works = db.session.execute(
        select(PhotoWork)
        .options(work_user_load)
        .join(PhotoWork.photographer)
        .join(Photographer.user)
        .where(
            PhotoWork.audit_status == PhotoWork.AUDIT_APPROVED,
            PhotoWork.status == 1,
            PhotoWork.is_featured == 1,
            User.status == 1,
        )
        .order_by(PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
        .limit(3)
    ).scalars().all()

    # 首页热门作品：审核通过、上架、摄影师账号正常，按热度分取前 8 个展示。
    hot_works = db.session.execute(
        select(PhotoWork)
        .options(work_user_load, work_images_load)
        .join(PhotoWork.photographer)
        .join(Photographer.user)
        .where(
            PhotoWork.audit_status == PhotoWork.AUDIT_APPROVED,
            PhotoWork.status == 1,
            User.status == 1,
        )
        .order_by(PhotoWork.hot_score.desc(), PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
        .limit(8)
    ).scalars().unique().all()

    # 首页最新作品：按发布时间倒序取最新 8 个。
    recent_works = db.session.execute(
        select(PhotoWork)
        .options(work_user_load)
        .join(PhotoWork.photographer)
        .join(Photographer.user)
        .where(
            PhotoWork.audit_status == PhotoWork.AUDIT_APPROVED,
            PhotoWork.status == 1,
            User.status == 1,
        )
        .order_by(PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
        .limit(8)
    ).scalars().all()

    # 推荐摄影师：只展示认证通过且用户账号正常的摄影师。
    photographers = db.session.execute(
        select(Photographer)
        .options(joinedload(Photographer.user))
        .join(Photographer.user)
        .where(
            Photographer.cert_status == Photographer.STATUS_APPROVED,
            User.status == 1,
        )
        .order_by(Photographer.create_time.desc(), Photographer.photographer_id.desc())
        .limit(6)
    ).scalars().all()

    # 首页公告弹窗：读取最新一条已发布公告。
    latest_announcement = db.session.execute(
        select(Announcement)
        .where(Announcement.status == 1)
        .order_by(Announcement.create_time.desc(), Announcement.announcement_id.desc())
        .limit(1)
    ).scalar_one_or_none()

    # 首页展示作品：随机取一个公开可见作品。当前模板可能只在部分设计中使用它。
    showcase_work = db.session.execute(
        select(PhotoWork)
        .options(work_user_load)
        .join(PhotoWork.photographer)
        .join(Photographer.user)
        .where(
            PhotoWork.audit_status == PhotoWork.AUDIT_APPROVED,
            PhotoWork.status == 1,
            User.status == 1,
        )
        .order_by(func.rand())
        .limit(1)
    ).scalar_one_or_none()

    # render_template 会去 templates/index.html 找模板。
    # 左边名字是模板中使用的变量名，右边是 Python 里查出来的数据变量。
    return render_template(
        'index.html',
        carousels=carousels,
        featured_works=featured_works,
        hot_works=hot_works,
        recent_works=recent_works,
        photographers=photographers,
        latest_announcement=latest_announcement,
        showcase_work=showcase_work,
    )


if __name__ == '__main__':
    app.run(debug=True)
