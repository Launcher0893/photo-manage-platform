# 摄影作品分享平台项目细节文档

## 1. 项目概述

本项目是一个基于 Flask 的“摄影作品分享平台”课程项目，核心目标是让普通用户、摄影师和管理员围绕摄影作品完成浏览、发布、互动和后台管理。

项目中存在三类主要角色：

- 普通用户：注册登录、浏览作品、查看摄影师、点赞评论作品、发帖、评论帖子、管理自己的帖子和个人资料。
- 摄影师用户：在普通用户能力基础上，提交或完善摄影师资料，认证通过后发布作品、编辑作品、上下架自己的作品。
- 管理员：登录后台控制台，管理用户、摄影师审核、作品、分类、论坛、公告、轮播图和系统日志。

整体技术路线是：

```text
浏览器页面
  -> Flask 路由
  -> SQLAlchemy ORM 查询 MySQL
  -> Jinja2 模板渲染 HTML
  -> Bootstrap + 少量 jQuery 提供页面样式与交互
  -> 图片上传先落本地 static/uploads，再上传阿里云 OSS
```

项目入口是 `app.py`。运行时先初始化 Flask 应用、读取配置、初始化数据库对象、注册登录管理和 CSRF 防护，再注册各业务蓝图。

关键入口代码：

```python
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
csrf = CSRFProtect()
csrf.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
```

蓝图注册代码：

```python
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
```

这说明项目采用“按业务模块拆分视图”的结构。前台作品、论坛、公告、摄影师等模块有自己的前台蓝图，后台模块通常使用 `/admin/<module>/...` 前缀。

## 2. 项目目录结构

项目根目录主要文件如下：

```text
photo-manage-platform/
├── app.py
├── config.py
├── db.py
├── models/
├── views/
├── templates/
├── utils/
├── static/
├── photo/
├── photo_manage_platform.sql
├── README.md
├── HANDOFF.md
├── photography-platform-design-plan.md
└── requirements.txt
```

### 2.1 根目录核心文件

`app.py` 是 Flask 应用入口，负责：

- 创建 Flask 应用对象。
- 读取 `Config` 配置。
- 初始化 `db`、`CSRFProtect`、`LoginManager`。
- 注册所有蓝图。
- 定义首页 `/`。
- 定义 `/photo/<path:filename>` 静态图片访问。

`config.py` 负责配置数据库、密钥、上传大小和 OSS 参数：

```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'photo-manage-platform-dev-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        DEFAULT_DATABASE_URL
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    MAX_IMAGE_SIZE = int(os.environ.get('MAX_IMAGE_SIZE', 5 * 1024 * 1024))

    OSS_ENABLED = os.environ.get('OSS_ENABLED', 'true').lower() not in ('0', 'false', 'no')
    OSS_ACCESS_KEY_ID = os.environ.get('OSS_ACCESS_KEY_ID', '')
    OSS_ACCESS_KEY_SECRET = os.environ.get('OSS_ACCESS_KEY_SECRET', '')
```

这里的设计重点是：数据库连接和 OSS 密钥可以通过环境变量或 `.env` 覆盖，不需要把真实密钥写死在代码里。

`db.py` 只创建一个 SQLAlchemy 实例：

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

这个实例被所有模型和视图共享，是 ORM 操作的基础。

`photo_manage_platform.sql` 是数据库建表和演示数据脚本。项目的表结构、外键、状态字段以这个 SQL 文件为准。

`requirements.txt` 记录依赖：

```text
Flask
Flask-SQLAlchemy
Flask-Login
Flask-WTF
PyMySQL
SQLAlchemy
oss2
python-dotenv
```

### 2.2 models 目录

`models/` 目录保存 SQLAlchemy 模型类，每张主要数据表对应一个模型文件。`models/__init__.py` 统一导入模型，方便视图层使用：

```python
from .Admin import Admin
from .Announcement import Announcement
from .Carousel import Carousel
from .Category import Category
from .ForumBoard import ForumBoard
from .ForumComment import ForumComment
from .ForumPost import ForumPost
from .ForumPostImage import ForumPostImage
from .ForumPostLike import ForumPostLike
from .PhotoWork import PhotoWork
from .PhotoWorkImage import PhotoWorkImage
from .Photographer import Photographer
from .Role import Role
from .SystemLog import SystemLog
from .User import User
from .WorkComment import WorkComment
from .WorkLike import WorkLike
```

### 2.3 views 目录

`views/` 目录按业务模块拆分路由：

- `auth.py`：登录、注册、退出、加载登录用户。
- `work.py`：作品列表、作品详情、摄影师作品管理、后台作品管理。
- `photographer.py`：摄影师列表、摄影师主页、后台摄影师审核。
- `forum.py`：论坛板块、帖子列表、发帖、编辑、评论、后台论坛管理。
- `announcement.py`：公告前台展示和后台公告管理。
- `carousel.py`：后台轮播图管理。
- `category.py`：后台作品分类管理。
- `user.py`：个人中心、资料编辑、用户后台管理。
- `dashboard.py`：后台控制台。
- `api.py`：作品点赞、评论和后台图表数据接口。
- `system.py`：系统日志列表。

### 2.4 templates 目录

`templates/` 保存 Jinja2 页面模板：

- `base.html`：前台公共布局和导航栏。
- `admin_base.html`：后台公共布局和侧边栏。
- `index.html`：首页。
- `work/`：作品前台与后台模板。
- `forum/`：论坛前台与后台模板。
- `user/`：个人中心和用户后台模板。
- `photographer/`：摄影师列表、详情和审核模板。
- `announcement/`：公告前台和后台模板。
- `carousel/`、`category/`、`dashboard/`、`system/`：后台功能页面。

前台模板继承 `base.html`，后台模板继承 `admin_base.html`。公共模板中还集中处理了 CSRF meta 和重复提交防护。

### 2.5 utils 目录

`utils/` 保存通用工具：

- `decorators.py`：普通用户和管理员权限装饰器。
- `encryption.py`：MD5 密码加密和旧明文密码兼容。
- `file_upload.py`：图片校验、本地保存、OSS 上传和删除。
- `oss_utils.py`：OSS bucket、URL、object key、上传删除逻辑。
- `logger.py`：后台操作日志。
- `pagination.py`、`demo_data.py`：辅助工具。

## 3. 数据库表与依赖关系

数据库使用 MySQL，ORM 使用 SQLAlchemy。主要表可以按业务分为用户权限、作品、论坛、内容运营和日志五组。

### 3.1 用户与管理员相关表

#### user

`user` 是普通用户和摄影师用户的基础表。

核心字段：

- `user_id`：主键。
- `username`：登录账号，唯一。
- `password`：密码，当前写入 MD5。
- `nickname`：昵称。
- `email`、`phone`、`avatar_url`：个人资料。
- `user_role`：用户角色，`1` 普通用户，`2` 摄影师。
- `status`：账号状态，`1` 正常，`0` 禁用，`-1` 软删除。
- `create_time`、`update_time`：创建和更新时间。

模型代码：

```python
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(30))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    avatar_url = db.Column(db.String(255))
    user_role = db.Column(db.SmallInteger, default=1)
    status = db.Column(db.SmallInteger, default=1)
```

`User` 继承 `UserMixin`，所以可以被 Flask-Login 识别。项目重写了 `get_id()`：

```python
def get_id(self):
    return f'user:{self.user_id}'
```

这样登录态中会保存 `user:<id>`，用于和管理员登录态区分。

#### photographer

`photographer` 是摄影师认证资料表，与 `user` 一对一。

核心字段：

- `photographer_id`：主键。
- `user_id`：关联 `user.user_id`，唯一。
- `real_name`：真实姓名。
- `city`：所在城市。
- `cert_status`：认证状态，`0` 待审核，`1` 通过，`2` 拒绝。
- `cert_remark`：审核备注。
- `audit_admin_id`：审核管理员。
- `audit_time`：审核时间。

模型关系：

```python
user = db.relationship('User', back_populates='photographer')
works = db.relationship(
    'PhotoWork',
    back_populates='photographer',
    lazy=True,
    passive_deletes='all',
)
```

`user` 与 `photographer` 的关系在 `User` 中也有对应定义：

```python
photographer = db.relationship(
    'Photographer',
    back_populates='user',
    uselist=False,
    passive_deletes='all',
)
```

这表示一个用户最多对应一条摄影师资料。

#### role 与 admin

`role` 是管理员角色表，`admin` 是管理员账号表。

`admin` 关联 `role`：

```python
role_id = db.Column(
    db.Integer,
    db.ForeignKey('role.role_id', ondelete='RESTRICT'),
    nullable=False
)
```

管理员模型也继承 `UserMixin`，但 `get_id()` 返回 `admin:<id>`。这和普通用户的 `user:<id>` 区分，统一登录时可以加载不同模型。

### 3.2 作品相关表

作品模块的核心链路是：

```text
user
  -> photographer
      -> photo_work
          -> photo_work_image
          -> work_like
          -> work_comment
category
  -> photo_work
```

#### category

作品分类表：

- `category_id`：主键。
- `category_name`：分类名称，唯一。
- `sort`：排序。
- `status`：启用状态。

一个分类可以对应多个作品：

```python
works = db.relationship(
    'PhotoWork',
    back_populates='category',
    lazy=True,
    passive_deletes='all',
)
```

#### photo_work

作品主表。

核心字段：

- `work_id`：主键。
- `title`：作品标题。
- `photographer_id`：摄影师 ID。
- `category_id`：分类 ID。
- `cover_url`：封面图 URL。
- `city`：拍摄城市。
- `description`：作品描述。
- `view_count`：浏览量。
- `like_count`：点赞数。
- `comment_count`：评论数。
- `hot_score`：热度分。
- `audit_status`：审核状态，`0` 待审，`1` 通过，`2` 拒绝。
- `is_featured`：是否首页精选。
- `status`：上下架状态。

模型关系：

```python
photographer = db.relationship('Photographer', back_populates='works')
category = db.relationship('Category', back_populates='works')
images = db.relationship('PhotoWorkImage', backref='photo_work', lazy=True, passive_deletes='all')
likes = db.relationship('WorkLike', back_populates='photo_work', lazy=True, passive_deletes='all')
comments = db.relationship('WorkComment', back_populates='photo_work', lazy=True, passive_deletes='all')
```

作品热度通过模型方法维护：

```python
def update_hot_score(self):
    self.hot_score = (self.view_count or 0) + (self.like_count or 0) * 3 + (self.comment_count or 0) * 2
```

项目中作品列表按热度排序时直接使用 `hot_score` 字段，这样不需要每次实时计算。

#### photo_work_image

作品组图表。

- `image_id`：主键。
- `work_id`：关联作品。
- `image_url`：图片 URL。
- `oss_object_name`：OSS 对象 key。
- `sort`：图片排序。

外键 `work_id` 使用 `ON DELETE CASCADE`，作品被删除时，数据库层面允许级联删除图片记录。

#### work_like

作品点赞表。

- `like_id`：主键。
- `work_id`：作品。
- `user_id`：点赞用户。
- `create_time`：点赞时间。

业务上通过查询 `(work_id, user_id)` 判断当前用户是否已点赞。点赞或取消后重新统计点赞数写回 `photo_work.like_count`。

#### work_comment

作品评论表。

- `comment_id`：主键。
- `work_id`：作品。
- `user_id`：评论用户。
- `content`：评论内容。
- `audit_status`：审核状态，当前评论提交默认通过。
- `status`：显示状态。

后台评论管理主要切换 `status`，并重新统计作品可见评论数。

### 3.3 论坛相关表

论坛模块的核心链路是：

```text
forum_board
  -> forum_post
      -> forum_post_image
      -> forum_post_like
      -> forum_comment
user
  -> forum_post / forum_comment / forum_post_like
```

#### forum_board

论坛板块表：

- `board_id`：主键。
- `board_name`：板块名。
- `description`：描述。
- `sort`：排序。
- `status`：启用状态。

一个板块对应多个帖子：

```python
posts = db.relationship('ForumPost', backref='forum_board', lazy=True, passive_deletes='all')
```

#### forum_post

帖子主表。

核心字段：

- `post_id`：主键。
- `board_id`：所属板块。
- `user_id`：发帖用户。
- `title`：标题。
- `content`：内容。
- `view_count`、`like_count`、`comment_count`：浏览、点赞、评论数。
- `is_top`：是否置顶。
- `status`：状态，`1` 正常，`0` 删除或隐藏。

模型关系：

```python
user = db.relationship('User', back_populates='forum_posts')
images = db.relationship('ForumPostImage', backref='forum_post', lazy=True, passive_deletes='all')
comments = db.relationship('ForumComment', backref='forum_post', lazy=True, passive_deletes='all')
likes = db.relationship(
    'ForumPostLike',
    back_populates='forum_post',
    lazy=True,
    passive_deletes='all',
)
```

#### forum_post_image

帖子图片表，结构和作品图片类似，保存图片 URL、OSS object key 和排序。

#### forum_post_like

帖子点赞表，记录用户对帖子的点赞关系。

#### forum_comment

帖子评论表。

- `post_id` 关联帖子。
- `user_id` 关联评论用户。
- `content` 保存评论内容。
- `status` 控制是否显示。

后台隐藏或恢复评论后，会重新统计帖子可见评论数。

### 3.4 内容运营表

#### announcement

公告表。

- `announcement_id`：主键。
- `title`：标题。
- `content`：内容。
- `cover_url`：封面。
- `admin_id`：发布管理员。
- `status`：发布状态。

前台只查询 `status == 1` 的公告。首页会读取最新一条已发布公告作为弹窗内容。

#### carousel

轮播图表。

- `carousel_id`：主键。
- `title`：标题。
- `image_url`：图片地址。
- `link_type`、`link_id`、`link_url`：跳转目标。
- `sort`：排序。
- `status`：启用状态。

首页只展示 `status == 1` 的轮播图。

### 3.5 系统日志表

`system_log` 记录后台管理员操作。

- `log_id`：主键。
- `admin_id`：管理员。
- `operate_type`：操作类型。
- `operate_content`：操作内容。
- `ip_address`：IP 地址。
- `operate_time`：操作时间。

写日志工具：

```python
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
```

这里做了两个保护：

- 只有管理员操作才写日志。
- 写日志失败不会影响主业务，异常时回滚日志写入。

### 3.6 外键依赖和删除策略

项目 SQL 中主要外键关系如下：

```text
admin.role_id -> role.role_id                    RESTRICT
announcement.admin_id -> admin.admin_id          RESTRICT
photographer.user_id -> user.user_id             RESTRICT
photographer.audit_admin_id -> admin.admin_id    SET NULL
photo_work.photographer_id -> photographer       RESTRICT
photo_work.category_id -> category               RESTRICT
photo_work_image.work_id -> photo_work           CASCADE
work_like.work_id -> photo_work                  CASCADE
work_like.user_id -> user                        CASCADE
work_comment.work_id -> photo_work               CASCADE
work_comment.user_id -> user                     CASCADE
forum_post.board_id -> forum_board               RESTRICT
forum_post.user_id -> user                       CASCADE
forum_post_image.post_id -> forum_post           CASCADE
forum_post_like.post_id -> forum_post            CASCADE
forum_post_like.user_id -> user                  CASCADE
forum_comment.post_id -> forum_post              CASCADE
forum_comment.user_id -> user                    CASCADE
system_log.admin_id -> admin                     RESTRICT
```

含义：

- `RESTRICT`：被引用的数据不能直接物理删除，例如有作品的摄影师、被作品使用的分类。
- `CASCADE`：主记录删除时从属记录可级联删除，例如作品图片、评论、点赞。
- `SET NULL`：管理员被删除时，摄影师审核记录中的审核人可置空。

当前业务上用户删除采用软删除：`user.status = -1`，不是物理删除用户记录。这样能保留作品、帖子、评论等历史数据的关系。

## 4. 功能模块与关键代码说明

### 4.1 登录、注册与权限控制

登录模块在 `views/auth.py`。项目使用统一登录入口 `/auth/login`，普通用户和管理员在同一个页面登录。

加载登录用户：

```python
def load_user(user_id: str):
    if not user_id:
        return None

    prefix, _, raw_id = user_id.partition(':')
    if raw_id.isdigit():
        if prefix == 'admin':
            return db.session.get(Admin, int(raw_id))
        if prefix == 'user':
            return db.session.get(User, int(raw_id))

    if user_id.isdigit():
        return db.session.get(User, int(user_id))

    return None
```

这里的关键点是登录 ID 带前缀：

- 普通用户：`user:<user_id>`。
- 管理员：`admin:<admin_id>`。

这样 Flask-Login 能在同一个登录系统里区分两个账号表。

登录逻辑：

```python
user = db.session.execute(
    select(User).where(User.username == username)
).scalar_one_or_none()
if user is not None and verify_password(user.password, password):
    if user.status != 1:
        flash('该账号已被禁用。', 'error')
        return render_template('login.html')

    if password_needs_upgrade(user.password, password):
        user.password = md5_encrypt(password)
        db.session.commit()

    login_user(user)
    flash('登录成功。', 'success')
    return redirect(url_for('index'))
```

如果普通用户不存在或密码不匹配，再查询管理员：

```python
admin = db.session.execute(
    select(Admin).where(Admin.admin_account == username)
).scalar_one_or_none()
if admin is not None and verify_password(admin.admin_password, password):
    if admin.status != 1:
        flash('该管理员账号已被禁用。', 'error')
        return render_template('login.html')

    login_user(admin)
    flash('管理员登录成功。', 'success')
    return redirect(url_for('dashboard.index'))
```

密码工具在 `utils/encryption.py`：

```python
def md5_encrypt(password):
    raw = '' if password is None else str(password)
    return hashlib.md5(raw.encode('utf-8')).hexdigest()

def verify_password(stored_password, raw_password):
    stored = str(stored_password)
    hashed = md5_encrypt(raw_password)
    if stored.lower() == hashed:
        return True
    return not is_md5_hash(stored) and stored == str(raw_password)
```

这里既支持 MD5 密码，也兼容旧演示数据中的明文密码；旧明文密码登录成功后会自动升级成 MD5。

权限装饰器在 `utils/decorators.py`：

```python
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if not getattr(current_user, 'is_admin', False):
            abort(403)
        if getattr(current_user, 'status', 0) != 1:
            logout_user()
            flash('账号已被禁用，请联系管理员。', 'error')
            return redirect(url_for('auth.login'))
        return view_func(*args, **kwargs)
    return wrapper
```

`user_required` 和 `admin_required` 的区别：

- `user_required`：要求登录且不是管理员。
- `admin_required`：要求登录且是管理员。

这样可以避免管理员进入普通用户发帖、点赞等页面，也避免普通用户访问后台。

### 4.2 首页

首页在 `app.py` 的 `/` 路由中实现。管理员访问首页时会直接跳后台：

```python
@app.route('/')
def index():
    if current_user.is_authenticated and getattr(current_user, 'is_admin', False):
        return redirect(url_for('dashboard.index'))
```

首页查询轮播图：

```python
carousels = db.session.execute(
    select(Carousel)
    .where(Carousel.status == 1)
    .order_by(Carousel.sort.asc(), Carousel.carousel_id.desc())
).scalars().all()
```

当前首页轮播图的后端数据仍来自 `carousel` 表，但前端展示方式已经改为 `templates/index.html` 中的自定义轮播组件，不使用 Bootstrap 默认 Carousel。模板会遍历 `carousels` 生成 `.carousel-slide` 和 `.carousel-dot`，再由页面底部的原生 JavaScript 控制当前图、上一张、下一张、隐藏图的位置 class。

轮播跳转地址由模板根据 `link_type` 生成：

```html
{% if carousel.link_type == 'work' and carousel.link_id %}
    {% set link_url = '/work/detail/' ~ carousel.link_id %}
{% elif carousel.link_type == 'photographer' and carousel.link_id %}
    {% set link_url = '/photographer/detail/' ~ carousel.link_id %}
{% elif carousel.link_type == 'announcement' and carousel.link_id %}
    {% set link_url = '/announcement/detail/' ~ carousel.link_id %}
{% elif carousel.link_type == 'url' and carousel.link_url %}
    {% set link_url = carousel.link_url %}
{% endif %}
```

每张轮播图会把跳转地址写入 `data-link`：

```html
<div class="carousel-slide" data-index="{{ loop.index0 }}" data-link="{{ link_url or '' }}" data-title="{{ carousel.title or '' }}">
    <img src="{{ carousel.image_url }}" alt="{{ carousel.title or '轮播图' }}">
</div>
```

前端 JavaScript 维护 `currentIndex`，通过左右按钮、圆点点击和自动播放切换轮播图；鼠标移入轮播区域会暂停自动播放，鼠标移出继续播放。

首页精选作品：

```python
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
```

这里同时过滤：

- 作品审核通过。
- 作品上架。
- 作品被管理员设为精选。
- 关联摄影师用户状态正常。

首页推荐摄影师：

```python
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
```

这保证禁用或软删除的摄影师不会在前台首页出现。

### 4.3 作品浏览、详情、点赞评论

作品前台列表在 `views/work.py` 的 `/work/list`。

查询条件：

```python
stmt = (
    select(PhotoWork)
    .options(
        joinedload(PhotoWork.category),
        joinedload(PhotoWork.photographer).joinedload(Photographer.user),
    )
    .join(PhotoWork.photographer)
    .join(Photographer.user)
    .where(
        PhotoWork.audit_status == PhotoWork.AUDIT_APPROVED,
        PhotoWork.status == 1,
        User.status == 1,
    )
)
```

支持关键词、分类、城市筛选：

```python
if keyword:
    stmt = stmt.where(PhotoWork.title.like(f'%{keyword}%'))
if category_id:
    stmt = stmt.where(PhotoWork.category_id == category_id)
if city:
    stmt = stmt.where(PhotoWork.city.like(f'%{city}%'))
```

排序逻辑：

```python
if sort_by == 'new':
    stmt = stmt.order_by(PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
else:
    stmt = stmt.order_by(PhotoWork.hot_score.desc(), PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
```

作品详情在 `/work/detail/<work_id>`。进入详情时会增加浏览量并更新热度：

```python
work.view_count = (work.view_count or 0) + 1
work.update_hot_score()
db.session.commit()
```

作品点赞接口在 `views/api.py`：

```python
@bp.route('/work/<int:work_id>/like', methods=['POST'])
def like_work(work_id):
    if not current_user.is_authenticated or getattr(current_user, 'is_admin', False):
        return jsonify({'success': False, 'message': '请先使用用户账号登录。'}), 401
```

点赞和取消点赞逻辑：

```python
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
```

点赞后重新统计数量：

```python
db.session.flush()
work.like_count = db.session.execute(
    select(func.count(WorkLike.like_id)).where(WorkLike.work_id == work_id)
).scalar_one()
work.update_hot_score()
db.session.commit()
```

评论接口同样在 `views/api.py`，评论提交后默认审核通过：

```python
db.session.add(
    WorkComment(
        work_id=work_id,
        user_id=current_user.user_id,
        content=content,
        audit_status=1,
        status=1,
    )
)
```

然后重新统计可见评论数：

```python
work.comment_count = db.session.execute(
    select(func.count(WorkComment.comment_id)).where(
        WorkComment.work_id == work_id,
        WorkComment.status == 1,
        WorkComment.audit_status == 1,
    )
).scalar_one()
work.update_hot_score()
db.session.commit()
```

### 4.4 摄影师作品管理

摄影师必须认证通过才能发布和管理作品。判断函数：

```python
def _approved_current_photographer():
    photographer = current_user.photographer
    if photographer is None or photographer.cert_status != Photographer.STATUS_APPROVED:
        return None
    return photographer
```

我的作品页面 `/work/my`：

```python
@bp.route('/my')
@user_required
def my_works():
    photographer = _approved_current_photographer()
    if photographer is None:
        flash('摄影师审核通过后才能管理作品。', 'error')
        return redirect(url_for('user.profile'))

    stmt = (
        select(PhotoWork)
        .options(joinedload(PhotoWork.category))
        .where(PhotoWork.photographer_id == photographer.photographer_id)
        .order_by(PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
    )
    works = db.paginate(stmt, page=page, per_page=10, error_out=False)
    return render_template('work/my_list.html', works=works)
```

发布和编辑作品共用一个路由函数：

```python
@bp.route('/add', methods=['GET', 'POST'])
@bp.route('/edit/<int:work_id>', methods=['GET', 'POST'])
@user_required
def photographer_form(work_id=None):
```

编辑时必须确保作品属于当前摄影师：

```python
work = db.session.execute(
    select(PhotoWork)
    .options(selectinload(PhotoWork.images))
    .where(
        PhotoWork.work_id == work_id,
        PhotoWork.photographer_id == photographer.photographer_id,
    )
).scalar_one_or_none()
if work is None:
    abort(404)
```

新建作品时设置默认状态：

```python
work = PhotoWork(
    photographer_id=photographer.photographer_id,
    status=1,
    audit_status=PhotoWork.AUDIT_APPROVED,
)
```

作品保存的公共逻辑在 `_save_work_from_request()`，它同时服务摄影师前台和管理员后台。主要流程是：

1. 从表单读取标题、分类、城市、描述。
2. 校验必填项。
3. 处理要删除的旧组图。
4. 保存或替换封面。
5. 保存新增组图。
6. 更新热度。
7. 提交数据库。
8. 删除被替换的旧图片文件。

关键代码：

```python
work.title = request.form.get('title', '').strip()
work.category_id = request.form.get('category_id', type=int)
work.city = request.form.get('city', '').strip() or None
work.description = request.form.get('description', '').strip() or None

if not work.title or not work.photographer_id or not work.category_id:
    flash('标题、摄影师和分类不能为空。', 'error')
    return render_template(template_name, work=work, categories=categories, **template_context)
```

处理旧图删除：

```python
delete_image_ids = {
    int(image_id)
    for image_id in request.form.getlist('delete_image_ids')
    if image_id.isdigit()
}
for image in list(getattr(work, 'images', []) or []):
    if image.image_id in delete_image_ids:
        deleted_images.append((image.image_url, image.oss_object_name))
        db.session.delete(image)
```

上传组图：

```python
for offset, image_file in enumerate(request.files.getlist('work_images'), start=1):
    image_upload = save_image_result(image_file, 'works')
    if image_upload:
        uploaded_results.append(image_upload)
        db.session.add(
            PhotoWorkImage(
                work_id=work.work_id,
                image_url=image_upload.url,
                oss_object_name=image_upload.oss_object_name,
                sort=current_max_sort + offset,
            )
        )
```

保存失败时会回滚并删除本次新上传的文件：

```python
try:
    db.session.commit()
except Exception:
    db.session.rollback()
    for upload in uploaded_results:
        delete_uploaded_file(upload.url, upload.oss_object_name)
```

摄影师上下架自己的作品：

```python
work = db.session.execute(
    select(PhotoWork).where(
        PhotoWork.work_id == work_id,
        PhotoWork.photographer_id == photographer.photographer_id,
    )
).scalar_one_or_none()
if work is None:
    abort(404)

work.status = 0 if work.status == 1 else 1
db.session.commit()
```

### 4.5 摄影师列表、主页和审核

摄影师前台列表在 `views/photographer.py`：

```python
stmt = (
    select(Photographer)
    .options(joinedload(Photographer.user), selectinload(Photographer.works))
    .join(Photographer.user)
    .where(
        Photographer.cert_status == Photographer.STATUS_APPROVED,
        User.status == 1,
    )
    .order_by(Photographer.create_time.desc(), Photographer.photographer_id.desc())
)
```

这保证前台只显示审核通过、账号正常的摄影师。

摄影师主页也做同样过滤：

```python
photographer = db.session.execute(
    select(Photographer)
    .options(joinedload(Photographer.user))
    .join(Photographer.user)
    .where(
        Photographer.photographer_id == photographer_id,
        Photographer.cert_status == Photographer.STATUS_APPROVED,
        User.status == 1,
    )
).scalar_one_or_none()
if photographer is None:
    abort(404)
```

后台摄影师审核：

```python
@admin_bp.route('/audit/<int:photographer_id>', methods=['GET', 'POST'])
@admin_required
def admin_audit(photographer_id):
```

提交审核结果：

```python
cert_status = request.form.get('cert_status', type=int)
if cert_status not in (Photographer.STATUS_APPROVED, Photographer.STATUS_REJECTED):
    flash('审核状态无效。', 'error')
    return render_template('photographer/admin_audit.html', photographer=photographer)

photographer.cert_status = cert_status
photographer.cert_remark = request.form.get('cert_remark', '').strip() or None
photographer.audit_admin_id = current_user.admin_id
photographer.audit_time = datetime.now()
if photographer.user:
    photographer.user.user_role = 2 if cert_status == Photographer.STATUS_APPROVED else photographer.user.user_role
db.session.commit()
```

审核通过时会把用户角色设为摄影师。

### 4.6 论坛板块、帖子和我的帖子

论坛板块页 `/forum/board` 查询启用板块，并统计每个板块正常帖子数：

```python
boards = db.session.execute(
    select(ForumBoard)
    .where(ForumBoard.status == 1)
    .order_by(ForumBoard.sort.asc(), ForumBoard.board_id.asc())
).scalars().all()
post_count_rows = db.session.execute(
    select(ForumPost.board_id, func.count(ForumPost.post_id))
    .where(ForumPost.status == 1)
    .group_by(ForumPost.board_id)
).all()
post_counts = {board_id: count for board_id, count in post_count_rows}
```

帖子列表 `/forum/post_list/<board_id>` 会先确认板块存在且启用：

```python
board_item = db.session.get(ForumBoard, board_id)
if board_item is None or board_item.status != 1:
    abort(404)
```

帖子列表只展示正常帖子：

```python
stmt = (
    select(ForumPost)
    .options(joinedload(ForumPost.user))
    .where(ForumPost.board_id == board_id, ForumPost.status == 1)
)
```

支持按热度或时间排序。热度是临时计算：

```python
hot_score = (
    func.coalesce(ForumPost.view_count, 0)
    + func.coalesce(ForumPost.like_count, 0) * 3
    + func.coalesce(ForumPost.comment_count, 0) * 2
)
```

帖子详情 `/forum/post_detail/<post_id>` 会增加浏览量：

```python
post.view_count = (post.view_count or 0) + 1
db.session.commit()
```

发帖路由支持两个入口：

```python
@bp.route('/post_add', methods=['GET', 'POST'])
@bp.route('/post_add/<int:board_id>', methods=['GET', 'POST'])
@user_required
def post_add(board_id=None):
```

发帖时校验板块、标题和内容：

```python
selected_board_id = request.form.get('board_id', type=int)
board_item = db.session.get(ForumBoard, selected_board_id) if selected_board_id else None
if board_item is None or board_item.status != 1:
    flash('请选择有效的论坛板块。', 'error')
    return render_template('forum/post_add.html', boards=boards, selected_board_id=selected_board_id)

title = request.form.get('title', '').strip()
content = request.form.get('content', '').strip()
if not title or not content:
    flash('标题和内容不能为空。', 'error')
    return render_template('forum/post_add.html', boards=boards, selected_board_id=selected_board_id)
```

创建帖子：

```python
post = ForumPost(
    board_id=selected_board_id,
    user_id=current_user.user_id,
    title=title,
    content=content,
    status=1,
)
db.session.add(post)
db.session.flush()
```

帖子图片上传：

```python
for sort, image_file in enumerate(request.files.getlist('post_images'), start=1):
    image_upload = save_image_result(image_file, 'forum')
    if image_upload:
        uploaded_results.append(image_upload)
        db.session.add(
            ForumPostImage(
                post_id=post.post_id,
                image_url=image_upload.url,
                oss_object_name=image_upload.oss_object_name,
                sort=sort,
            )
        )
```

编辑帖子时必须是作者本人：

```python
post = db.session.execute(
    select(ForumPost)
    .options(selectinload(ForumPost.images))
    .where(ForumPost.post_id == post_id, ForumPost.status == 1)
).scalar_one_or_none()
if post is None:
    abort(404)
if post.user_id != current_user.user_id:
    abort(403)
```

我的帖子页面 `/forum/my`：

```python
@bp.route('/my')
@user_required
def my_posts():
    page = request.args.get('page', default=1, type=int)
    stmt = (
        select(ForumPost)
        .options(joinedload(ForumPost.forum_board))
        .where(ForumPost.user_id == current_user.user_id)
        .order_by(ForumPost.create_time.desc(), ForumPost.post_id.desc())
    )
    posts = db.paginate(stmt, page=page, per_page=10, error_out=False)
    return render_template('forum/my_list.html', posts=posts)
```

这个页面显示当前用户所有帖子，包括正常和已删除状态，方便恢复。

用户自己的帖子删除或恢复：

```python
@bp.route('/post_status/<int:post_id>', methods=['POST'])
@user_required
def toggle_my_post_status(post_id):
    post = db.session.execute(
        select(ForumPost).where(
            ForumPost.post_id == post_id,
            ForumPost.user_id == current_user.user_id,
        )
    ).scalar_one_or_none()
    if post is None:
        abort(404)

    post.status = 0 if post.status == 1 else 1
    db.session.commit()
    flash('帖子状态已更新。', 'success')
    return redirect(url_for('forum.my_posts'))
```

### 4.7 论坛点赞和评论

帖子点赞接口在 `views/forum.py`：

```python
@bp.route('/post_like/<int:post_id>', methods=['POST'])
def post_like(post_id):
    if not current_user.is_authenticated or getattr(current_user, 'is_admin', False):
        return jsonify({'success': False, 'message': '请先使用用户账号登录。'}), 401
```

它和作品点赞类似，先判断是否已经点赞，再新增或删除点赞记录，最后重新统计 `like_count`。

帖子评论：

```python
@bp.route('/comment_add/<int:post_id>', methods=['POST'])
@user_required
def comment_add(post_id):
    post = db.session.get(ForumPost, post_id)
    if post is None or post.status != 1:
        abort(404)
    content = request.form.get('content', '').strip()
    if not content:
        flash('评论内容不能为空。', 'error')
        return redirect(url_for('forum.post_detail', post_id=post_id))

    db.session.add(ForumComment(post_id=post_id, user_id=current_user.user_id, content=content, status=1))
```

评论后重新统计可见评论数：

```python
post.comment_count = db.session.scalar(
    select(func.count(ForumComment.comment_id)).where(
        ForumComment.post_id == post_id,
        ForumComment.status == 1,
    )
) or 0
db.session.commit()
```

### 4.8 用户中心和资料编辑

用户中心在 `views/user.py` 的 `/user/profile`。

如果当前用户是认证通过的摄影师，会查询自己的作品：

```python
photographer = current_user.photographer if current_user.user_role == User.ROLE_PHOTOGRAPHER else None
my_works = []
if photographer is not None and photographer.cert_status == Photographer.STATUS_APPROVED:
    my_works = db.session.execute(
        select(PhotoWork)
        .options(joinedload(PhotoWork.category))
        .where(PhotoWork.photographer_id == photographer.photographer_id)
        .order_by(PhotoWork.create_time.desc(), PhotoWork.work_id.desc())
    ).scalars().all()
```

用户中心也查询自己的正常帖子：

```python
my_posts = db.session.execute(
    select(ForumPost)
    .options(joinedload(ForumPost.forum_board))
    .where(ForumPost.user_id == current_user.user_id, ForumPost.status == 1)
    .order_by(ForumPost.create_time.desc(), ForumPost.post_id.desc())
).scalars().all()
```

编辑个人资料：

```python
current_user.nickname = request.form.get('nickname', '').strip() or current_user.username
current_user.email = request.form.get('email', '').strip() or None
current_user.phone = request.form.get('phone', '').strip() or None
avatar_url = save_image(request.files.get('avatar_file'), 'avatars')
if avatar_url:
    old_avatar_url = current_user.avatar_url
    current_user.avatar_url = avatar_url
```

完善摄影师资料：

```python
photographer.real_name = request.form.get('real_name', '').strip() or None
photographer.city = request.form.get('city', '').strip() or None
if photographer.cert_status == Photographer.STATUS_REJECTED:
    photographer.cert_status = Photographer.STATUS_PENDING
    photographer.cert_remark = None
db.session.commit()
```

如果之前审核被拒绝，重新保存资料后状态会回到待审核。

### 4.9 管理员控制台

控制台在 `views/dashboard.py`。它统计平台关键指标：

```python
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
```

热门作品：

```python
hot_works = db.session.execute(
    select(PhotoWork)
    .where(PhotoWork.status == 1)
    .order_by(PhotoWork.hot_score.desc(), PhotoWork.work_id.desc())
    .limit(10)
).scalars().all()
```

热门帖子：

```python
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
```

后台图表数据接口在 `views/api.py`：

```python
@bp.route('/dashboard/trends')
@admin_required
def dashboard_trends():
```

它生成最近 7 天的日期列表，并按日期聚合用户数和作品数：

```python
days = [today - timedelta(days=offset) for offset in range(6, -1, -1)]
start_dt = datetime.combine(days[0], datetime.min.time())

user_rows = db.session.execute(
    select(func.date(User.create_time), func.count(User.user_id))
    .where(User.create_time >= start_dt)
    .group_by(func.date(User.create_time))
).all()
```

返回 JSON：

```python
return jsonify({
    'labels': labels,
    'users': [user_map.get(key, 0) for key in keys],
    'works': [work_map.get(key, 0) for key in keys],
})
```

### 4.10 后台作品、用户、分类、论坛管理

后台作品列表支持标题、审核状态、上下架状态、精选状态筛选：

```python
if title:
    stmt = stmt.where(PhotoWork.title.like(f'%{title}%'))
if audit_status in (0, 1, 2):
    stmt = stmt.where(PhotoWork.audit_status == audit_status)
if status in (0, 1):
    stmt = stmt.where(PhotoWork.status == status)
if is_featured in (0, 1):
    stmt = stmt.where(PhotoWork.is_featured == is_featured)
```

后台作品审核接口：

```python
@admin_bp.route('/<int:work_id>/audit', methods=['POST'])
@admin_required
def audit(work_id):
    work = db.session.get(PhotoWork, work_id)
    if work is None:
        return jsonify({'success': False, 'message': '作品不存在。'}), 404
    audit_status = request.form.get('audit_status', type=int)
    if audit_status not in (PhotoWork.AUDIT_APPROVED, PhotoWork.AUDIT_REJECTED):
        return jsonify({'success': False, 'message': '审核状态无效。'}), 400
    work.audit_status = audit_status
    db.session.commit()
```

后台用户管理支持软删除：

```python
@admin_bp.route('/delete/<int:user_id>', methods=['POST'])
@admin_required
def soft_delete(user_id):
    user = db.session.get(User, user_id)
    if user is not None:
        user.status = -1
        db.session.commit()
        log_admin_action('用户删除', f'删除用户：{user.username}')
```

恢复用户：

```python
@admin_bp.route('/restore/<int:user_id>', methods=['POST'])
@admin_required
def restore(user_id):
    user = db.session.get(User, user_id)
    if user is not None:
        user.status = 1
        db.session.commit()
```

分类管理使用统一新增/编辑路由：

```python
@bp.route('/add', methods=['GET', 'POST'])
@bp.route('/edit/<int:category_id>', methods=['GET', 'POST'])
@admin_required
def form(category_id=None):
```

论坛后台包含帖子、板块、评论：

- `/admin/forum/post_list`：帖子列表。
- `/admin/forum/board_list`：板块列表。
- `/admin/forum/comment_list`：评论列表。
- `/admin/forum/post/top/<post_id>`：置顶或取消置顶。
- `/admin/forum/post/status/<post_id>`：隐藏或恢复帖子。
- `/admin/forum/comment/status/<comment_id>`：隐藏或恢复评论。

后台隐藏评论后会同步更新帖子评论数：

```python
comment.status = 0 if comment.status == 1 else 1
post = db.session.get(ForumPost, comment.post_id)
if post is not None:
    post.comment_count = db.session.scalar(
        select(func.count(ForumComment.comment_id)).where(
            ForumComment.post_id == post.post_id,
            ForumComment.status == 1,
        )
    ) or 0
db.session.commit()
```

### 4.11 公告和轮播图

公告前台列表只展示已发布公告：

```python
stmt = (
    select(Announcement)
    .where(Announcement.status == 1)
    .order_by(Announcement.create_time.desc(), Announcement.announcement_id.desc())
)
```

后台公告新增和编辑共用一个表单函数：

```python
@admin_bp.route('/add', methods=['GET', 'POST'])
@admin_bp.route('/edit/<int:announcement_id>', methods=['GET', 'POST'])
@admin_required
def admin_form(announcement_id=None):
```

保存公告时可上传封面：

```python
cover_url = save_image(request.files.get('cover_file'), 'announcements')
if cover_url:
    old_cover_url = announcement.cover_url
    announcement.cover_url = cover_url
```

删除公告时会删除数据库记录，并尝试删除封面文件：

```python
title = announcement.title
cover_url = announcement.cover_url
db.session.delete(announcement)
db.session.commit()
delete_ok = delete_uploaded_file(cover_url)
```

轮播图后台功能在 `views/carousel.py`。它支持新增、编辑、启用停用和删除。后台保存的数据包括标题、图片 URL、跳转类型、跳转 ID、外部链接、排序和状态。

首页读取启用轮播图后，在 `templates/index.html` 中使用自定义三图位移式轮播展示。当前轮播的主要效果是：

- 中间显示当前主图，左右显示上一张和下一张预览图。
- 非当前图片通过缩放、透明度和模糊效果弱化。
- 左右按钮可以切换图片。
- 下方圆点可以跳转指定图片。
- 默认每 5 秒自动切换一次。
- 鼠标悬停暂停自动播放，移出后继续播放。
- 点击轮播图可根据后台配置跳转到作品、摄影师、公告或外部链接。

因此，轮播图的数据管理仍然在后台完成，展示动画和交互则由首页模板中的 CSS 和原生 JavaScript 完成。

### 4.12 图片上传与 OSS

上传入口在 `utils/file_upload.py`。

允许的图片格式：

```python
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
```

上传流程：

```python
def save_image_result(file: Optional[FileStorage], folder: str) -> Optional[UploadResult]:
    if file is None or not file.filename:
        return None
    if not allowed_image(file.filename):
        raise ValueError('Only image files are allowed.')
```

检查文件大小：

```python
max_size = int(current_app.config.get('MAX_IMAGE_SIZE', 50 * 1024 * 1024))
file.stream.seek(0, 2)
file_size = file.stream.tell()
file.stream.seek(0)
if max_size > 0 and file_size > max_size:
    raise ValueError(f'Image file must not exceed {max_size // 1024 // 1024}MB.')
```

生成安全文件名并保存本地：

```python
original_name = secure_filename(file.filename)
suffix = original_name.rsplit('.', 1)[1].lower()
filename = f'{uuid4().hex}.{suffix}'

upload_root = Path(current_app.static_folder) / 'uploads' / folder
upload_root.mkdir(parents=True, exist_ok=True)
local_path = upload_root / filename
file.save(local_path)
```

如果未启用 OSS，直接返回本地 URL：

```python
local_url = url_for('static', filename=f'uploads/{folder}/{filename}')
if not oss_enabled():
    return UploadResult(url=local_url, filename=filename, local_path=local_path)
```

如果启用 OSS，上传到 OSS 并返回 OSS URL：

```python
object_key = build_oss_object_key(folder, filename)
try:
    oss_url = upload_file_to_oss(local_path, object_key)
except Exception as exc:
    local_path.unlink(missing_ok=True)
    raise ValueError(str(exc)) from exc
```

OSS 工具在 `utils/oss_utils.py`：

```python
def get_oss_bucket():
    import oss2
    access_key_id = current_app.config.get('OSS_ACCESS_KEY_ID')
    access_key_secret = current_app.config.get('OSS_ACCESS_KEY_SECRET')
    endpoint = current_app.config.get('OSS_ENDPOINT')
    bucket_name = current_app.config.get('OSS_BUCKET_NAME')
```

配置缺失时抛出明确错误：

```python
missing = [
    name for name, value in (
        ('OSS_ACCESS_KEY_ID', access_key_id),
        ('OSS_ACCESS_KEY_SECRET', access_key_secret),
        ('OSS_ENDPOINT', endpoint),
        ('OSS_BUCKET_NAME', bucket_name),
    )
    if not value or str(value).startswith('YOUR_')
]
if missing:
    raise RuntimeError(f'Missing OSS config: {", ".join(missing)}')
```

构造 OSS object key：

```python
def build_oss_object_key(folder: str, filename: str) -> str:
    prefix = _clean_path_part(current_app.config.get('OSS_UPLOAD_PREFIX', ''))
    folder = _clean_path_part(folder)
    filename = _clean_path_part(filename)
    parts = [part for part in (prefix, folder, filename) if part]
    return str(PurePosixPath(*parts))
```

### 4.13 CSRF 和重复提交防护

项目在 `app.py` 中启用 Flask-WTF CSRF：

```python
csrf = CSRFProtect()
csrf.init_app(app)
```

CSRF 错误处理：

```python
@app.errorhandler(CSRFError)
def handle_csrf_error(error):
    message = 'CSRF 校验失败，请刷新页面后重试。'
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accept_mimetypes.best == 'application/json':
        return jsonify({'success': False, 'message': message}), 400
    return message, 400
```

前台基础模板中提供 meta：

```html
<meta name="csrf-token" content="{{ csrf_token() }}">
```

Ajax 请求统一带 CSRF 请求头：

```javascript
var csrfToken = $('meta[name="csrf-token"]').attr('content');
if (csrfToken) {
    $.ajaxSetup({
        headers: { 'X-CSRFToken': csrfToken }
    });
}
```

普通 POST 表单中都放隐藏字段：

```html
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
```

基础模板还做了重复提交防护，提交后禁用按钮：

```javascript
$('form[method="POST"], form[method="post"]').on('submit', function() {
    var $form = $(this);
    if ($form.data('submitting')) {
        return false;
    }
    $form.data('submitting', true);
    $form.find('button[type="submit"], input[type="submit"]').each(function() {
        var $button = $(this);
        $button.data('original-text', $button.is('input') ? $button.val() : $button.text());
        if ($button.is('input')) {
            $button.val('处理中...');
        } else {
            $button.text('处理中...');
        }
        $button.prop('disabled', true);
    });
    return true;
});
```

## 5. 技术栈在项目中的使用方式

### 5.1 Flask

Flask 是项目的 Web 框架，负责：

- 定义 URL 路由。
- 接收 GET/POST 请求。
- 调用数据库查询。
- 使用 `render_template()` 渲染 HTML。
- 使用 `redirect()` 和 `url_for()` 控制跳转。
- 使用 `jsonify()` 返回 Ajax 接口数据。

典型路由：

```python
@bp.route('/list')
def list_page():
    page = request.args.get('page', default=1, type=int)
    stmt = select(PhotoWork)
    works = db.paginate(stmt, page=page, per_page=9, error_out=False)
    return render_template('work/list.html', works=works)
```

### 5.2 Blueprint

Blueprint 用于把项目拆成多个模块，避免所有路由都堆在 `app.py`。

前台作品蓝图：

```python
bp = Blueprint('work', __name__, url_prefix='/work')
```

后台作品蓝图：

```python
admin_bp = Blueprint('admin_work', __name__, url_prefix='/admin/work')
```

这样同一个业务模块可以清楚地区分前台和后台：

- 前台：`/work/list`、`/work/detail/<id>`。
- 后台：`/admin/work/list`、`/admin/work/edit/<id>`。

### 5.3 SQLAlchemy ORM

SQLAlchemy 让代码用 Python 类操作数据库表。

定义表：

```python
class ForumPost(db.Model):
    __tablename__ = 'forum_post'

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    board_id = db.Column(db.Integer, db.ForeignKey('forum_board.board_id', ondelete='RESTRICT'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
```

查询数据：

```python
posts = db.session.execute(
    select(ForumPost)
    .where(ForumPost.board_id == board_id, ForumPost.status == 1)
    .order_by(ForumPost.create_time.desc())
).scalars().all()
```

分页：

```python
posts = db.paginate(stmt, page=page, per_page=10, error_out=False)
```

关系加载：

```python
select(PhotoWork).options(
    joinedload(PhotoWork.category),
    joinedload(PhotoWork.photographer).joinedload(Photographer.user),
)
```

`joinedload` 和 `selectinload` 用于减少模板访问关联对象时的额外查询。

### 5.4 Flask-Login

Flask-Login 管理登录态。

初始化：

```python
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
```

注册用户加载函数：

```python
@login_manager.user_loader
def user_loader(user_id):
    return load_user(user_id)
```

登录：

```python
login_user(user)
```

退出：

```python
logout_user()
```

模板和视图里可以使用 `current_user` 判断当前用户。

### 5.5 Flask-WTF CSRF

Flask-WTF 提供跨站请求伪造防护。项目中所有 POST 表单都需要提交 `csrf_token`，Ajax 请求也要带 `X-CSRFToken`。

这可以防止用户在已登录状态下，被恶意页面诱导自动提交后台操作。

### 5.6 MySQL 与 PyMySQL

MySQL 是持久化数据库，`PyMySQL` 是 Python 连接 MySQL 的驱动。连接串在 `config.py`：

```python
DEFAULT_DATABASE_URL = (
    'mysql+pymysql://root:Sean20041218@127.0.0.1:3306/'
    'photo_manage_platform?charset=utf8mb4'
)
```

实际运行时建议用 `.env` 覆盖：

```env
DATABASE_URL=mysql+pymysql://root:your_password@127.0.0.1:3306/photo_manage_platform?charset=utf8mb4
```

### 5.7 Jinja2 模板

Jinja2 负责把后端传来的数据渲染成 HTML。

继承模板：

```html
{% extends 'base.html' %}
{% block title %}我的作品{% endblock %}
{% block content %}
...
{% endblock %}
```

循环数据：

```html
{% for work in works.items %}
    <tr>
        <td>{{ work.title }}</td>
        <td>{{ work.category.category_name if work.category else '未分类' }}</td>
    </tr>
{% else %}
    <tr>
        <td colspan="8" class="text-center text-muted">暂无作品</td>
    </tr>
{% endfor %}
```

Jinja2 的 `if`、`for`、变量输出让页面可以根据登录角色、数据状态动态展示。

### 5.8 Bootstrap

Bootstrap 用于页面布局和组件样式。

项目中常见用法：

- `container`：页面内容宽度控制。
- `navbar`：顶部导航。
- `row`、`col-md-*`：响应式网格。
- `card`：作品、帖子、统计卡片。
- `table`：后台列表。
- `btn`：按钮。
- `modal`：弹窗表单。
- `pagination`：分页。

例如“我的作品”和“我的帖子”页面都使用 Bootstrap 表格和分页来展示管理列表。

需要注意的是，当前首页轮播图不是 Bootstrap 默认 Carousel，而是项目在 `templates/index.html` 中自定义的轮播组件。Bootstrap 在首页主要负责整体布局、按钮、弹窗等基础样式。

### 5.9 jQuery / Ajax

jQuery 主要用于：

- Ajax 点赞。
- Ajax 评论。
- 首页公告弹窗本地记录。
- 全局 CSRF 请求头。
- 表单重复提交防护。

作品或帖子点赞不刷新整个页面，而是通过 Ajax 请求接口，然后更新按钮和数量。

首页自定义轮播主要使用原生 JavaScript，不依赖 jQuery。它通过 `querySelectorAll()` 获取轮播图和圆点，通过 `addEventListener()` 绑定左右按钮、圆点和图片点击事件，通过 `setInterval()` 自动播放。核心逻辑是给不同图片切换这些 CSS 类：

```text
position-prev
position-current
position-next
position-hidden-left
position-hidden-right
```

这些类控制图片的位置、缩放、透明度、模糊和层级，从而形成中间主图、两侧预览图的轮播效果。

### 5.10 阿里云 OSS

OSS 用于保存上传图片。项目不是直接把图片二进制存进 MySQL，而是：

```text
上传文件
  -> 保存到 static/uploads/<module>/
  -> 上传到 OSS
  -> 数据库保存图片 URL 和 oss_object_name
```

这样数据库只保存字符串路径，图片由对象存储负责托管，更适合图片类平台。

### 5.11 python-dotenv

`python-dotenv` 让项目启动时读取根目录 `.env`：

```python
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if load_dotenv is not None:
    load_dotenv(os.path.join(BASE_DIR, '.env'))
```

这样本机数据库密码和 OSS 密钥可以写在 `.env`，并且 `.env` 已加入 `.gitignore`，不会提交到仓库。

## 6. 主要路由清单

### 6.1 前台路由

```text
/                         首页
/auth/login               统一登录
/auth/register            注册
/auth/logout              退出
/work/list                作品列表
/work/detail/<work_id>    作品详情
/work/add                 摄影师发布作品
/work/edit/<work_id>      摄影师编辑作品
/work/my                  我的作品
/work/status/<work_id>    我的作品上下架
/photographer/list        摄影师列表
/photographer/detail/<id> 摄影师主页
/forum/board              论坛板块
/forum/post_list/<id>     板块帖子列表
/forum/post_add           发布帖子
/forum/post_add/<id>      在指定板块发帖
/forum/post_edit/<id>     编辑自己的帖子
/forum/post_detail/<id>   帖子详情
/forum/my                 我的帖子
/forum/post_status/<id>   删除或恢复自己的帖子
/announcement/list        公告列表
/announcement/detail/<id> 公告详情
/user/profile             个人中心
/user/edit_profile        编辑资料
/user/edit_photographer   完善摄影师资料
/user/change_password     修改密码
```

### 6.2 后台路由

```text
/admin/dashboard/                 控制台
/admin/work/list                  作品管理
/admin/work/add                   新增作品
/admin/work/edit/<id>             编辑作品
/admin/work/<id>/audit            审核作品
/admin/work/comment_list          作品评论管理
/admin/photographer/list          摄影师审核列表
/admin/photographer/audit/<id>    摄影师审核
/admin/category/list              分类管理
/admin/user/list                  用户管理
/admin/user/detail/<id>           用户详情
/admin/forum/post_list            论坛帖子管理
/admin/forum/board_list           论坛板块管理
/admin/forum/comment_list         论坛评论管理
/admin/announcement/list          公告管理
/admin/carousel/list              轮播图管理
/admin/system/logs                系统日志
```

### 6.3 API 路由

```text
/api/work/<work_id>/like          作品点赞/取消点赞
/api/work/<work_id>/comment       作品评论
/api/dashboard/trends             后台用户和作品趋势
/api/dashboard/forum_activity     后台论坛趋势
/api/dashboard/category_stats     后台分类作品统计
/forum/post_like/<post_id>        帖子点赞/取消点赞
```

## 7. 页面模板对应关系

常见路由和模板对应：

```text
/                         templates/index.html
/auth/login               templates/login.html
/auth/register            templates/register.html
/work/list                templates/work/list.html
/work/detail/<id>         templates/work/detail.html
/work/add, /work/edit     templates/work/form.html
/work/my                  templates/work/my_list.html
/forum/board              templates/forum/board.html
/forum/post_list/<id>     templates/forum/post_list.html
/forum/post_detail/<id>   templates/forum/post_detail.html
/forum/post_add/edit      templates/forum/post_add.html
/forum/my                 templates/forum/my_list.html
/user/profile             templates/user/profile.html
/announcement/list        templates/announcement/list.html
/announcement/detail/<id> templates/announcement/detail.html
/admin/dashboard/         templates/dashboard/index.html
```

前台页面继承：

```html
{% extends 'base.html' %}
```

后台页面继承：

```html
{% extends 'admin_base.html' %}
```

## 8. 运行方式与验证

### 8.1 安装依赖

```powershell
cd "D:\Program Files\Code\PyCharm\photo-manage-platform"
python -m pip install -r requirements.txt
```

### 8.2 导入数据库

先在 MySQL 中创建数据库 `photo_manage_platform`，再导入 SQL：

```powershell
& 'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe' -uroot -p你的密码 --default-character-set=utf8mb4 photo_manage_platform --execute="source D:/Program Files/Code/PyCharm/photo-manage-platform/photo_manage_platform.sql"
```

### 8.3 启动项目

```powershell
python app.py
```

默认访问：

```text
http://127.0.0.1:5000/
```

### 8.4 演示账号

```text
admin / 123456
user1 / 123456
user2 / 123456
user3 / 123456
user_test / 123456
```

### 8.5 常用检查命令

Python 编译检查：

```powershell
python -m compileall app.py views models utils
```

模板语法检查：

```powershell
python -c "from pathlib import Path; from jinja2 import Environment, FileSystemLoader; env=Environment(loader=FileSystemLoader('templates')); [env.parse(p.read_text(encoding='utf-8')) for p in Path('templates').rglob('*.html')]; print('jinja syntax ok')"
```

Flask 模板加载检查：

```powershell
python -c "from pathlib import Path; from app import app; [app.jinja_env.get_template(p.relative_to('templates').as_posix()) for p in Path('templates').rglob('*.html')]; print('flask jinja load/compile ok')"
```

核心路由冒烟检查：

```powershell
python -c "from app import app; c=app.test_client(); paths=['/','/work/list','/photographer/list','/forum/board','/announcement/list','/auth/login']; print([(p,c.get(p).status_code) for p in paths])"
```

后台路由检查：

```powershell
python -c "from app import app; c=app.test_client(); c.post('/auth/login', data={'username':'admin','password':'123456'}); paths=['/admin/dashboard/','/admin/work/comment_list','/admin/forum/board_list','/admin/system/logs']; print([(p,c.get(p).status_code) for p in paths])"
```

## 9. 设计特点与维护注意事项

### 9.1 前后台分离在路由层实现

项目不是前后端分离架构，而是 Flask 服务端渲染。前台和后台通过不同蓝图、不同 URL 前缀和不同基础模板区分：

- 前台：`/work/...`、`/forum/...`、`/photographer/...`。
- 后台：`/admin/work/...`、`/admin/forum/...`、`/admin/dashboard/...`。

### 9.2 公开内容必须过滤状态

前台公开展示作品和摄影师时，通常需要同时过滤：

- 作品审核通过。
- 作品上架。
- 摄影师审核通过。
- 用户状态正常。

例如作品列表：

```python
.where(
    PhotoWork.audit_status == PhotoWork.AUDIT_APPROVED,
    PhotoWork.status == 1,
    User.status == 1,
)
```

后续新增公开页面时也应保持这个规则。

### 9.3 删除以状态切换为主

用户删除是软删除：

```python
user.status = -1
```

作品、帖子、评论多采用状态切换：

```python
status = 0 if status == 1 else 1
```

这样方便后台恢复，也避免破坏演示数据和外键关系。

### 9.4 图片删除需要同时考虑 OSS 和本地副本

删除上传文件时应优先使用：

```python
delete_uploaded_file(file_url, oss_object_name)
```

不要只删除数据库记录。否则 OSS 或本地 `static/uploads` 中可能残留无用图片。

### 9.5 POST 表单必须带 CSRF

所有普通表单 POST 都应包含：

```html
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
```

Ajax POST 依赖基础模板中的 `X-CSRFToken` 设置。


## 10. 总结

本项目是一个完整的 Flask 服务端渲染课程项目，核心业务围绕摄影作品和摄影师社区展开。它使用 SQLAlchemy 管理 MySQL 数据，使用 Flask-Login 管理普通用户和管理员登录态，使用 Flask-WTF 做 CSRF 防护，使用 Bootstrap 构建页面，使用 OSS 保存图片资源。

从代码结构看，项目已经形成较清晰的模块边界：

- `models/` 负责数据结构。
- `views/` 负责路由和业务流程。
- `templates/` 负责页面展示。
- `utils/` 负责权限、上传、加密、日志等通用能力。
- `photo_manage_platform.sql` 负责数据库结构和演示数据。

理解这个项目时，可以按三条主线阅读：

1. 用户主线：注册登录、个人中心、发帖、点赞评论。
2. 摄影师主线：认证、发布作品、作品管理。
3. 管理员主线：后台审核、内容管理、数据统计、系统日志。

这三条主线共同构成了“摄影作品分享平台”的完整业务闭环。
