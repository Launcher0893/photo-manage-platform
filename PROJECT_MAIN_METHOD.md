# 摄影作品分享平台项目主方法

本文档用于快速理解本 Flask 课程项目。阅读项目时不要从所有文件逐个硬看，而是按“URL -> 路由 -> 模型 -> 模板 -> 前端交互”的主线追踪。

## 1. 总体链路

一次页面访问的完整流程：

```text
浏览器访问 URL
-> Flask 根据路由找到 Python 函数
-> 路由函数读取请求参数
-> SQLAlchemy 查询或修改 MySQL
-> render_template 把数据交给 HTML 模板
-> Jinja 模板生成 HTML
-> Bootstrap/CSS/JS 在浏览器中显示和交互
```

本项目核心目录：

```text
app.py                         Flask 入口，初始化 app、数据库、登录、CSRF、蓝图和首页
config.py                      数据库、SECRET_KEY、上传大小、OSS 配置
db.py                          SQLAlchemy 全局 db 对象
models/*.py                    数据库表对应的模型类
views/*.py                     路由和业务逻辑
templates/**/*.html            Jinja 页面模板
utils/*.py                     权限、加密、上传、OSS、日志等工具
photo_manage_platform.sql      MySQL 建表和演示数据
```

## 2. 先从 URL 找路由

Flask 项目中，路由就是“URL 和 Python 函数”的对应关系。

示例：首页在 `app.py`：

```python
@app.route('/')
def index():
    ...
```

表示访问 `/` 时执行 `index()`。

蓝图会给一组路由统一加前缀。例如 `views/work.py`：

```python
bp = Blueprint('work', __name__, url_prefix='/work')

@bp.route('/list')
def list_page():
    ...
```

最终完整地址是：

```text
/work/list
```

常用模块对应关系：

```text
/auth/...             views/auth.py，登录、注册、退出
/work/...             views/work.py，前台作品
/admin/work/...       views/work.py，后台作品管理
/photographer/...     views/photographer.py，摄影师展示
/admin/photographer   views/photographer.py，摄影师审核
/forum/...            views/forum.py，前台论坛
/admin/forum/...      views/forum.py，后台论坛管理
/announcement/...     views/announcement.py，前台公告
/admin/announcement   views/announcement.py，后台公告管理
/admin/carousel/...   views/carousel.py，轮播图管理
/admin/category/...   views/category.py，分类管理
/user/...             views/user.py，个人中心
/admin/user/...       views/user.py，后台用户管理
/api/...              views/api.py，Ajax JSON 接口
```

## 3. 再看路由函数做了什么

路由函数通常做 5 件事：

```text
1. 读取请求参数：request.args / request.form / request.files
2. 做权限或状态判断
3. 查询或修改数据库
4. flash 提示或返回 JSON
5. render_template 渲染模板，或 redirect 跳转
```

GET 和 POST 的区别：

```text
GET   通常用于打开页面、查询列表、查看详情
POST  通常用于提交表单、登录、保存、删除、状态切换、点赞评论
```

示例：登录 `/auth/login`：

```text
GET  /auth/login   显示 login.html
POST /auth/login   读取账号密码，查 user/admin 表，成功后 login_user()
```

示例：作品列表 `/work/list`：

```text
读取 keyword/category_id/city/sort_by/page
查询审核通过、上架、摄影师账号正常的作品
分页
渲染 templates/work/list.html
```

## 4. 模型就是数据库表的 Python 表达

`models/*.py` 里的类对应 MySQL 表。

例如 `models/User.py`：

```python
class User(db.Model, UserMixin):
    __tablename__ = 'user'
```

表示 `User` 类对应数据库 `user` 表。

字段对应关系：

```text
db.Integer       MySQL int
db.String(50)    MySQL varchar(50)
db.Text          MySQL text
db.DateTime      MySQL datetime
primary_key      主键
unique           唯一
nullable=False   不能为空
default          默认值
```

外键示例：

```python
photographer_id = db.Column(
    db.Integer,
    db.ForeignKey('photographer.photographer_id', ondelete='RESTRICT'),
    nullable=False
)
```

表示一个作品属于一个摄影师。

`relationship` 不是数据库字段，而是 Python 中访问关联对象的快捷方式。例如：

```python
work.photographer.user.nickname
work.category.category_name
```

## 5. 模板负责把数据变成页面

项目模板使用 Jinja。基础模板：

```text
templates/base.html         前台公共模板，导航栏、Bootstrap、公共 JS
templates/admin_base.html   后台公共模板，侧边栏、后台样式、公共 JS
```

子模板通常第一行是：

```jinja2
{% extends 'base.html' %}
```

或：

```jinja2
{% extends 'admin_base.html' %}
```

常用 Jinja 语法：

```jinja2
{{ work.title }}                         输出变量
{% for work in hot_works %}...{% endfor %} 循环
{% if current_user.is_authenticated %}...{% endif %} 判断
```

后端传给模板的数据来自 `render_template`：

```python
return render_template(
    'index.html',
    hot_works=hot_works,
    photographers=photographers,
)
```

模板里就能直接使用 `hot_works` 和 `photographers`。

## 6. 权限主线

项目权限由 Flask-Login 和自定义装饰器控制。

当前登录用户：

```python
current_user
```

判断登录：

```python
current_user.is_authenticated
```

判断管理员：

```python
getattr(current_user, 'is_admin', False)
```

权限装饰器：

```text
@admin_required   只允许管理员访问
@user_required    只允许前台用户访问，管理员不能访问
```

用户角色：

```text
User.ROLE_NORMAL = 1          普通用户
User.ROLE_PHOTOGRAPHER = 2    摄影师用户
```

摄影师审核状态：

```text
Photographer.STATUS_PENDING = 0    待审核
Photographer.STATUS_APPROVED = 1   审核通过
Photographer.STATUS_REJECTED = 2   审核拒绝
```

发布作品必须满足：

```text
已登录前台用户
user_role = 2
存在 photographer 记录
photographer.cert_status = 1
```

## 7. 图片上传主线

所有图片上传统一走：

```text
utils/file_upload.py
utils/oss_utils.py
```

上传流程：

```text
HTML 表单 enctype="multipart/form-data"
-> request.files 读取文件
-> save_image_result() 校验格式和大小
-> 保存到 static/uploads/<folder>/
-> 如果 OSS_ENABLED=true，再上传到 OSS
-> 数据库保存 URL 和 oss_object_name
```

业务目录：

```text
avatars         用户头像
works           作品封面和组图
forum           论坛帖子图片
announcements   公告封面
carousels       轮播图
```

如果演示环境不想连接 OSS，可在 `.env` 中设置：

```env
OSS_ENABLED=false
```

## 8. Ajax、CSRF 和前端交互

项目启用了 CSRF 防护：

```python
csrf = CSRFProtect()
csrf.init_app(app)
```

普通 POST 表单需要隐藏字段：

```html
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
```

Ajax 请求由 `base.html` 和 `admin_base.html` 自动加请求头：

```javascript
headers: { 'X-CSRFToken': csrfToken }
```

典型 Ajax 接口：

```text
POST /api/work/<work_id>/like       作品点赞/取消点赞
POST /api/work/<work_id>/comment    作品评论
POST /forum/post_like/<post_id>     帖子点赞/取消点赞
```

## 9. 读任何功能的固定方法

遇到一个功能，按下面顺序查：

```text
1. 先确定 URL
2. 在 app.py 或 views/*.py 找 @route
3. 看路由函数读取了哪些参数
4. 看它查询或修改了哪些 models
5. 看 render_template 使用了哪个模板
6. 看模板继承 base.html 还是 admin_base.html
7. 看是否有 JS/Ajax 参与
8. 看是否需要 @admin_required、@user_required 或摄影师审核状态
```

示例：理解作品详情页：

```text
URL: /work/detail/<work_id>
路由: views/work.py -> detail(work_id)
模型: PhotoWork、Photographer、User、WorkComment、WorkLike
模板: templates/work/detail.html
交互: 点赞和评论走 views/api.py
权限: 页面公开可看，点赞/评论需要前台用户登录
```

## 10. 当前项目核心主线总结

```text
首页
-> app.py index()
-> 读取轮播图、精选作品、热门作品、最新作品、摄影师、公告
-> templates/index.html

登录注册
-> views/auth.py
-> User/Admin/Photographer
-> templates/login.html、register.html

作品
-> views/work.py + views/api.py
-> PhotoWork、PhotoWorkImage、WorkLike、WorkComment
-> templates/work/*.html

论坛
-> views/forum.py
-> ForumBoard、ForumPost、ForumPostImage、ForumPostLike、ForumComment
-> templates/forum/*.html

后台
-> /admin/*
-> @admin_required
-> templates/admin_base.html
-> 用户、作品、摄影师、分类、论坛、公告、轮播图、日志管理
```
