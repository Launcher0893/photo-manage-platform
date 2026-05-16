# 摄影作品分享平台答辩分工与提问准备

## 1. 使用说明

这份文档用于答辩时按成员负责板块进行准备。当前先用“成员 A、成员 B、成员 C、成员 D、成员 E”占位，你们可以在答辩前把占位名称替换成真实姓名。

建议使用方式：

- 每位同学重点熟悉自己负责板块的页面、代码文件、数据库表和问答。
- 所有人都要看最后的“公共高频问题”，因为老师可能会从项目整体、数据库、权限、安全、上传等角度追问。
- 如果老师问到跨模块问题，先由对应模块负责人回答，再由项目架构负责人补充整体逻辑。

## 2. 总体分工表

| 成员 | 负责板块 | 重点页面/路由 | 核心代码文件 | 相关数据库表 |
| --- | --- | --- | --- | --- |
| 肖卓 | 项目架构、登录注册、权限控制、基础配置 | `/`、`/auth/login`、`/auth/register` | `app.py`、`config.py`、`views/auth.py`、`utils/decorators.py`、`utils/encryption.py` | `user`、`admin`、`role` |
| 王鹏睿 | 作品展示、作品详情、点赞评论、摄影师作品管理 | `/work/list`、`/work/detail/<id>`、`/work/my`、`/work/add` | `views/work.py`、`views/api.py`、`models/PhotoWork.py` | `photo_work`、`photo_work_image`、`work_like`、`work_comment`、`category` |
| 李孟祥 | 摄影师、个人中心、用户资料、摄影师认证资料 | `/photographer/list`、`/photographer/detail/<id>`、`/user/profile` | `views/photographer.py`、`views/user.py`、`models/Photographer.py`、`models/User.py` | `photographer`、`user`、`photo_work`、`forum_post` |
| 成员 D | 论坛、发帖、我的帖子、帖子评论点赞、论坛后台 | `/forum/board`、`/forum/post_list/<id>`、`/forum/post_add`、`/forum/my` | `views/forum.py`、`models/ForumPost.py`、`templates/forum/*.html` | `forum_board`、`forum_post`、`forum_post_image`、`forum_post_like`、`forum_comment` |
| 成员 E | 管理员后台、公告、轮播、分类、系统日志、统计图表 | `/admin/dashboard/`、`/admin/announcement/list`、`/admin/carousel/list` | `views/dashboard.py`、`views/announcement.py`、`views/carousel.py`、`views/category.py`、`views/system.py` | `announcement`、`carousel`、`category`、`system_log`、`admin` |

## 3. 成员 A：项目架构、登录注册、权限控制

### 负责范围

成员 A 负责讲清楚项目怎么启动、Flask 应用怎么组织、蓝图怎么注册、数据库怎么配置、普通用户和管理员怎么共用登录入口、权限如何隔离。

### 重点文件

- `app.py`：项目入口、扩展初始化、蓝图注册、首页。
- `config.py`：数据库、密钥、OSS、上传大小配置。
- `db.py`：SQLAlchemy 实例。
- `views/auth.py`：登录、注册、退出、用户加载。
- `utils/decorators.py`：普通用户和管理员权限装饰器。
- `utils/encryption.py`：MD5 加密和旧明文密码兼容。
- `templates/base.html`：前台导航栏。
- `templates/login.html`、`templates/register.html`：登录注册页面。

### 重点数据库表

- `user`：普通用户和摄影师用户账号。
- `admin`：管理员账号。
- `role`：管理员角色。

### 可演示页面

- `/auth/login`：统一登录入口。
- `/auth/register`：用户注册。
- `/`：首页。
- 管理员登录后 `/admin/dashboard/`：后台控制台。

### 老师可能问：这个项目的入口在哪里？

答：项目入口是 `app.py`。里面创建 Flask 应用，读取 `Config` 配置，初始化 `db`、`CSRFProtect`、`LoginManager`，然后注册各个业务蓝图，比如 `work_bp`、`forum_bp`、`admin_work_bp`、`admin_forum_bp`。最后通过 `app.run(debug=True)` 启动项目。

### 老师可能问：为什么要用 Blueprint？

答：因为项目功能比较多，如果所有路由都写在 `app.py` 会非常混乱。Blueprint 可以按模块拆分，比如作品模块在 `views/work.py`，论坛模块在 `views/forum.py`，后台作品管理用 `/admin/work` 前缀。这样前台和后台路由边界清楚，也方便维护。

### 老师可能问：普通用户和管理员为什么能共用一个登录页？

答：登录逻辑在 `views/auth.py`。用户提交账号密码后，系统先查 `user` 表，如果匹配就登录普通用户；如果不匹配再查 `admin` 表，如果匹配就登录管理员。普通用户登录后进入首页，管理员登录后进入后台控制台。

### 老师可能问：怎么区分当前登录的是用户还是管理员？

答：项目给登录 ID 加了前缀。普通用户的 `get_id()` 返回 `user:<id>`，管理员返回 `admin:<id>`。`load_user()` 根据前缀去查询 `User` 或 `Admin` 模型。代码里还通过 `is_admin` 属性判断当前身份。

### 老师可能问：权限控制怎么做？

答：权限控制主要在 `utils/decorators.py`。`admin_required` 要求当前用户已登录并且是管理员，否则跳转登录或返回 403；`user_required` 要求当前用户是普通用户身份，管理员不能进入普通用户操作页面。后台路由都加了 `@admin_required`，普通用户功能加 `@user_required`。

### 老师可能问：密码怎么保存？

答：项目使用 MD5 保存密码。`utils/encryption.py` 中有 `md5_encrypt()`。另外考虑到旧演示数据可能是明文，`verify_password()` 兼容旧明文密码，如果旧密码登录成功，会自动升级为 MD5。

### 老师可能问：数据库连接在哪里配置？

答：在 `config.py`。默认连接本地 MySQL 的 `photo_manage_platform` 数据库，也支持通过环境变量或 `.env` 中的 `DATABASE_URL` 覆盖，这样不同电脑可以使用自己的数据库账号密码。

## 4. 成员 B：作品模块、点赞评论、摄影师作品管理

### 负责范围

成员 B 负责讲清楚作品从展示、筛选、详情、浏览量、点赞评论，到摄影师发布作品、编辑作品、上下架作品的完整流程。

### 重点文件

- `views/work.py`：作品列表、详情、摄影师作品管理、后台作品管理。
- `views/api.py`：作品点赞、作品评论、后台图表接口。
- `models/PhotoWork.py`：作品模型。
- `models/PhotoWorkImage.py`：作品图片模型。
- `models/WorkLike.py`：作品点赞模型。
- `models/WorkComment.py`：作品评论模型。
- `templates/work/list.html`：作品列表。
- `templates/work/detail.html`：作品详情。
- `templates/work/form.html`：作品发布/编辑。
- `templates/work/my_list.html`：我的作品。

### 重点数据库表

- `photo_work`：作品主表。
- `photo_work_image`：作品组图表。
- `work_like`：作品点赞表。
- `work_comment`：作品评论表。
- `category`：作品分类表。
- `photographer`：作品所属摄影师。

### 可演示页面

- `/work/list`：作品列表。
- `/work/detail/<work_id>`：作品详情。
- `/work/add`：摄影师发布作品。
- `/work/my`：我的作品。

### 老师可能问：作品列表怎么筛选？

答：作品列表在 `views/work.py` 的 `list_page()`。它从请求参数读取 `keyword`、`category_id`、`city`、`sort_by`，然后用 SQLAlchemy 拼接查询条件。前台只展示审核通过、上架、且摄影师用户状态正常的作品。

### 老师可能问：作品为什么要过滤用户状态？

答：因为摄影师账号如果被管理员禁用或软删除，前台不应该继续展示这个摄影师的作品。所以作品查询会连接 `Photographer.user`，并加上 `User.status == 1`。

### 老师可能问：作品热度是怎么计算的？

答：热度字段在 `PhotoWork` 模型里维护。公式是浏览量加点赞数乘 3，再加评论数乘 2。每次浏览、点赞或评论后调用 `update_hot_score()` 更新热度，这样列表排序时可以直接按 `hot_score` 排序。

### 老师可能问：点赞功能怎么实现？

答：作品点赞接口在 `views/api.py` 的 `/api/work/<work_id>/like`。先判断用户是否登录且不是管理员，再查询 `work_like` 表中是否已有当前用户对该作品的点赞记录。如果没有就新增，有就删除。操作后重新统计点赞数写回 `photo_work.like_count`。

### 老师可能问：评论功能怎么实现？

答：作品评论接口在 `/api/work/<work_id>/comment`。接口校验登录状态、作品是否存在、评论内容是否为空。通过后新增 `WorkComment`，当前项目中评论默认 `audit_status=1`、`status=1`，然后重新统计可见评论数并更新作品热度。

### 老师可能问：摄影师发布作品时怎么保证只能管理自己的作品？

答：发布或编辑作品前会调用 `_approved_current_photographer()` 判断当前用户是不是审核通过的摄影师。编辑作品时查询条件里同时限制 `PhotoWork.work_id == work_id` 和 `PhotoWork.photographer_id == 当前摄影师ID`，如果查不到就返回 404。

### 老师可能问：作品图片上传怎么处理？

答：上传逻辑通过 `utils/file_upload.py` 的 `save_image_result()`。它先校验文件类型和大小，然后保存到 `static/uploads/works`，如果启用了 OSS，再上传到阿里云 OSS，数据库保存图片 URL 和 OSS object key。作品封面和组图都走这个流程。

## 5. 成员 C：摄影师模块、个人中心、用户资料

### 负责范围

成员 C 负责讲清楚摄影师列表和主页如何展示、摄影师认证资料如何维护、个人中心展示哪些数据、用户资料和头像如何修改。

### 重点文件

- `views/photographer.py`：摄影师列表、详情、后台审核。
- `views/user.py`：个人中心、资料编辑、摄影师资料编辑、用户后台管理。
- `models/User.py`：用户模型。
- `models/Photographer.py`：摄影师模型。
- `templates/photographer/list.html`：摄影师列表。
- `templates/photographer/detail.html`：摄影师主页。
- `templates/user/profile.html`：个人中心。

### 重点数据库表

- `user`：账号和个人资料。
- `photographer`：摄影师认证资料。
- `photo_work`：摄影师作品。
- `forum_post`：用户帖子。

### 可演示页面

- `/photographer/list`：摄影师列表。
- `/photographer/detail/<photographer_id>`：摄影师主页。
- `/user/profile`：个人中心。
- `/user/edit_profile`：编辑资料接口。
- `/user/edit_photographer`：完善摄影师资料接口。

### 老师可能问：普通用户和摄影师用户有什么区别？

答：普通用户和摄影师用户都在 `user` 表中，区别是 `user_role` 字段。`1` 表示普通用户，`2` 表示摄影师。摄影师还会在 `photographer` 表中有一条认证资料，审核通过后才可以发布作品。

### 老师可能问：摄影师列表为什么只显示部分用户？

答：摄影师列表查询 `photographer` 表，并连接 `user` 表。条件要求 `Photographer.cert_status == 1`，也就是认证通过，同时要求 `User.status == 1`，也就是账号正常。这样待审核、被拒绝、禁用或删除的摄影师都不会公开展示。

### 老师可能问：摄影师主页展示哪些内容？

答：摄影师主页展示摄影师基本信息和该摄影师已公开作品。作品查询会限制 `photographer_id`，并且要求作品审核通过、作品上架、关联用户状态正常。

### 老师可能问：个人中心怎么查询我的作品和我的帖子？

答：个人中心在 `views/user.py` 的 `profile()`。如果当前用户是审核通过的摄影师，就查询 `PhotoWork` 中当前摄影师的作品；同时查询 `ForumPost` 中当前用户发布且状态正常的帖子，然后传给 `templates/user/profile.html` 渲染。

### 老师可能问：编辑资料为什么改成弹窗？

答：个人中心模板中使用 Bootstrap modal。点击“编辑资料”或“完善摄影师资料”不会跳转到新页面，而是在当前页面弹出表单。表单仍然提交到 `/user/edit_profile` 或 `/user/edit_photographer`，后端逻辑保持不变。

### 老师可能问：头像上传怎么实现？

答：编辑资料时从 `request.files.get('avatar_file')` 获取头像文件，调用 `save_image()` 保存。保存成功后把返回的 URL 写入 `current_user.avatar_url`，如果替换了旧头像，会调用 `delete_uploaded_file(old_avatar_url)` 删除旧文件。

### 老师可能问：摄影师资料被拒绝后还能重新提交吗？

答：可以。`edit_photographer()` 中如果检测到当前认证状态是拒绝状态，再次保存资料时会把 `cert_status` 改回待审核，并清空 `cert_remark`，等待管理员重新审核。

## 6. 成员 D：论坛模块、发帖、我的帖子、论坛后台

### 负责范围

成员 D 负责讲清楚论坛板块、帖子列表、帖子详情、发帖编辑、帖子图片、评论点赞、我的帖子和论坛后台管理。

### 重点文件

- `views/forum.py`：论坛前台和后台全部核心逻辑。
- `models/ForumBoard.py`：论坛板块模型。
- `models/ForumPost.py`：帖子模型。
- `models/ForumPostImage.py`：帖子图片模型。
- `models/ForumPostLike.py`：帖子点赞模型。
- `models/ForumComment.py`：帖子评论模型。
- `templates/forum/board.html`：论坛板块页。
- `templates/forum/post_list.html`：帖子列表。
- `templates/forum/post_detail.html`：帖子详情。
- `templates/forum/post_add.html`：发帖/编辑。
- `templates/forum/my_list.html`：我的帖子。

### 重点数据库表

- `forum_board`：论坛板块。
- `forum_post`：帖子主表。
- `forum_post_image`：帖子图片。
- `forum_post_like`：帖子点赞。
- `forum_comment`：帖子评论。
- `user`：发帖人和评论人。

### 可演示页面

- `/forum/board`：论坛板块。
- `/forum/post_list/<board_id>`：板块帖子列表。
- `/forum/post_add`：发布帖子。
- `/forum/post_detail/<post_id>`：帖子详情。
- `/forum/my`：我的帖子。
- `/admin/forum/post_list`：后台帖子管理。
- `/admin/forum/board_list`：后台板块管理。
- `/admin/forum/comment_list`：后台评论管理。

### 老师可能问：论坛板块页的帖子数怎么统计？

答：板块页在 `views/forum.py` 的 `board()`。先查询所有启用板块，再从 `forum_post` 表按 `board_id` 分组统计 `status == 1` 的帖子数量。这样板块外面显示的帖子数和点进去看到的正常帖子列表保持一致。

### 老师可能问：帖子列表怎么排序？

答：帖子列表支持按热度和按时间排序。热度通过 SQL 表达式计算：浏览量加点赞数乘 3，再加评论数乘 2。同时置顶帖子会排在前面，之后再按热度或发布时间排序。

### 老师可能问：发布帖子时怎么选择板块？

答：发帖页面会查询所有启用的 `forum_board`，在表单中以下拉框展示。提交时后端根据 `board_id` 查询板块，并验证板块存在且启用，防止提交无效板块。

### 老师可能问：编辑帖子怎么保证只能编辑自己的？

答：编辑帖子时先查询状态正常的帖子，再判断 `post.user_id != current_user.user_id`。如果不是本人发布，就返回 403。这样用户不能通过修改 URL 编辑别人的帖子。

### 老师可能问：我的帖子页面和个人中心有什么区别？

答：个人中心只展示一部分正常帖子，主要作为概览；`/forum/my` 是独立的帖子管理页面，仿照“我的作品”页面，有完整表格、分页、查看、编辑、删除/恢复操作，并且会显示当前用户所有帖子，包括已删除状态。

### 老师可能问：帖子删除是真删除吗？

答：不是物理删除。用户点击删除时调用 `/forum/post_status/<id>`，把 `forum_post.status` 在 `1` 和 `0` 之间切换。这样帖子可以恢复，也不会破坏评论、点赞、图片等关联数据。

### 老师可能问：帖子评论数怎么维护？

答：新增评论后会重新统计当前帖子 `status == 1` 的评论数量，并写回 `forum_post.comment_count`。后台隐藏或恢复评论时，也会重新统计评论数，保证列表和详情显示一致。

### 老师可能问：论坛后台可以做什么？

答：论坛后台可以管理帖子、板块和评论。帖子可以隐藏/恢复、置顶/取消置顶；板块可以新增、编辑、启用停用；评论可以隐藏或恢复。所有后台操作都需要管理员权限。

## 7. 成员 E：管理员后台、公告、轮播、分类、日志、统计

### 负责范围

成员 E 负责讲清楚后台控制台、统计数据、公告管理、轮播图、分类管理、系统日志，以及管理员端公共界面。

### 重点文件

- `views/dashboard.py`：后台控制台数据。
- `views/announcement.py`：公告前台和后台。
- `views/carousel.py`：轮播图管理。
- `views/category.py`：分类管理。
- `views/system.py`：系统日志。
- `views/api.py`：后台图表数据接口。
- `utils/logger.py`：后台操作日志。
- `templates/admin_base.html`：后台公共布局。
- `templates/dashboard/index.html`：后台首页。

### 重点数据库表

- `admin`：管理员账号。
- `system_log`：系统日志。
- `announcement`：公告。
- `carousel`：轮播图。
- `category`：作品分类。
- `photo_work`、`forum_post`、`user`：后台统计数据来源。

### 可演示页面

- `/admin/dashboard/`：后台控制台。
- `/admin/announcement/list`：公告管理。
- `/admin/carousel/list`：轮播图管理。
- `/admin/category/list`：分类管理。
- `/admin/system/logs`：系统日志。

### 老师可能问：后台控制台统计了哪些数据？

答：控制台统计作品总数、用户总数、已认证摄影师、待审核摄影师、热门作品、待审核摄影师列表、最新用户、最新作品、热门帖子和分类作品数。这些数据来自 `dashboard.py` 中的 SQLAlchemy 聚合查询。

### 老师可能问：后台图表数据怎么来的？

答：图表数据由 `views/api.py` 提供，比如 `/api/dashboard/trends` 返回最近 7 天用户和作品增长趋势，`/api/dashboard/forum_activity` 返回论坛帖子和评论趋势，`/api/dashboard/category_stats` 返回分类作品统计。前端图表根据这些 JSON 数据渲染。

### 老师可能问：公告是怎么展示的？

答：公告表是 `announcement`。前台公告列表只查询 `status == 1` 的公告。首页会读取最新一条已发布公告，通过弹窗展示。后台可以新增、编辑、上下架和删除公告。

### 老师可能问：公告删除时图片怎么处理？

答：删除公告时先保存公告标题和封面 URL，然后删除数据库记录并提交，之后调用 `delete_uploaded_file(cover_url)` 尝试删除封面图片。如果图片删除失败，会提示“公告已删除，但封面图片删除失败”。

### 老师可能问：轮播图如何控制是否显示？

答：轮播图数据保存在 `carousel` 表。首页只查询 `status == 1` 的轮播图，并按 `sort` 排序。后台可以新增、编辑、启用停用和删除轮播图。前台首页会把这些数据传给 `templates/index.html`，再由自定义轮播组件展示。

### 老师可能问：首页轮播图为什么不用 Bootstrap 默认 Carousel？

答：因为当前首页设计需要中间主图、左右预览图、缩放、透明度、模糊、圆点切换、左右按钮、自动播放和点击跳转等效果。Bootstrap 默认 Carousel 更适合单张横幅切换，所以这里在 `index.html` 中自定义了 CSS 和原生 JavaScript 轮播逻辑。

### 老师可能问：首页轮播图点击后跳转到哪里？

答：跳转地址由后台轮播图的 `link_type` 和 `link_id` 决定。`work` 跳到作品详情，`photographer` 跳到摄影师主页，`announcement` 跳到公告详情，`url` 跳到外部链接。模板会把生成好的地址放到每张轮播图的 `data-link` 属性，点击图片时 JavaScript 读取这个属性并跳转。

### 老师可能问：分类被作品使用后能不能随便删除？

答：当前分类主要通过状态启用或停用，不做物理删除。数据库中 `photo_work.category_id` 对 `category.category_id` 是 `RESTRICT` 关系，说明被作品引用的分类不适合直接物理删除，否则会破坏作品数据。

### 老师可能问：系统日志记录哪些操作？

答：后台管理操作会调用 `log_admin_action()` 写入 `system_log`，包括操作管理员、操作类型、操作内容、IP 地址和时间。比如公告保存、作品状态切换、摄影师审核、论坛板块状态切换等。

### 老师可能问：后台页面怎么保证普通用户不能访问？

答：后台所有路由都加了 `@admin_required`。这个装饰器会检查是否登录、是否是管理员、账号是否正常。普通用户访问后台会返回 403，未登录会跳转登录页。

## 8. 公共高频问题

### 问：这个项目使用了哪些技术栈？

答：后端使用 Python Flask，数据库使用 MySQL，ORM 使用 SQLAlchemy，登录态使用 Flask-Login，CSRF 防护使用 Flask-WTF，页面使用 Jinja2 服务端渲染，前端样式使用 Bootstrap，交互部分使用 jQuery/Ajax 和原生 JavaScript，比如点赞评论用 Ajax，首页自定义轮播用原生 JavaScript，图片上传使用阿里云 OSS。

### 问：前台和后台是前后端分离吗？

答：不是。这个项目是 Flask 服务端渲染项目。后端查询数据库后用 Jinja2 模板直接生成 HTML 页面。只有点赞、评论、后台图表等少量功能使用 JSON 接口和 Ajax。

### 问：项目怎么启动？

答：先安装 `requirements.txt` 中的依赖，再导入 `photo_manage_platform.sql` 到 MySQL 数据库，确认 `.env` 或 `config.py` 中数据库连接正确，然后运行 `python app.py`，访问 `http://127.0.0.1:5000/`。

### 问：SQLAlchemy 模型和数据库表是什么关系？

答：`models/` 中每个模型类对应数据库中的一张表，比如 `User` 对应 `user`，`PhotoWork` 对应 `photo_work`，`ForumPost` 对应 `forum_post`。模型中的 `db.Column` 对应表字段，`db.relationship` 用于描述表之间的关联关系。

### 问：为什么要有 `photo_manage_platform.sql`？

答：这是项目的数据库建表和演示数据脚本。首次运行前需要导入它，里面包含表结构、外键约束和基础演示账号数据。项目的真实数据库结构以这个 SQL 文件为准。

### 问：为什么使用软删除？

答：用户、帖子、作品等数据之间有关联关系。如果直接物理删除，可能破坏作品、评论、点赞、帖子等历史数据。软删除通过 `status` 字段隐藏数据，既能保留关系，又方便管理员恢复。

### 问：CSRF 是什么？项目怎么防护？

答：CSRF 是跨站请求伪造，攻击者可能诱导已登录用户提交非法请求。项目使用 Flask-WTF 的 `CSRFProtect`，所有 POST 表单都带 `csrf_token`，Ajax 请求通过 `X-CSRFToken` 请求头提交。

### 问：图片为什么不直接存数据库？

答：图片文件体积大，直接存数据库会影响性能和维护。项目把图片保存到本地上传目录并上传到 OSS，数据库只保存图片 URL 和 OSS object key，这样更适合图片分享平台。

### 问：管理员和普通用户登录态会不会混淆？

答：不会。普通用户登录 ID 是 `user:<id>`，管理员登录 ID 是 `admin:<id>`。`load_user()` 会根据前缀查不同表，并且权限装饰器会进一步限制用户或管理员能访问的路由。

### 问：项目中哪里用了事务或异常处理？

答：图片上传和作品保存中比较明显。比如保存作品时如果数据库提交失败，会 `db.session.rollback()`，并删除本次新上传的图片，避免数据库失败但文件残留。日志写入失败也会 rollback，且不影响主业务。

### 问：如果老师问你负责模块外的问题怎么办？

答：先回答自己知道的整体逻辑，再把细节交给对应负责人。例如问到“帖子评论数为什么正确”，可以先说“评论数在新增或隐藏评论后重新统计”，再由论坛负责人补充具体代码在 `views/forum.py`。

## 9. 答辩演示顺序建议

建议按下面顺序演示，逻辑比较自然：

1. 成员 A：打开首页，说明项目结构、登录入口、普通用户和管理员身份区分。
2. 成员 B：进入作品列表和作品详情，演示筛选、浏览、点赞评论；再用摄影师账号展示发布作品和我的作品。
3. 成员 C：展示摄影师列表、摄影师主页、个人中心、资料编辑弹窗、摄影师资料。
4. 成员 D：展示论坛板块、帖子列表、发帖、帖子详情、我的帖子、删除恢复帖子。
5. 成员 E：切换管理员账号，展示后台控制台、作品/论坛/公告/轮播/分类/日志管理。

如果时间有限，优先演示：

- 登录和角色区分。
- 作品列表和详情。
- 摄影师发布作品。
- 论坛发帖和我的帖子。
- 管理员后台审核和管理。

## 10. 每位成员答辩前检查清单

### 成员 A

- 能说明 `app.py` 初始化流程。
- 能说明普通用户和管理员怎么共用登录入口。
- 能说明 `admin_required` 和 `user_required` 的区别。
- 能说明数据库连接配置在哪里。

### 成员 B

- 能说明作品列表筛选和排序。
- 能说明点赞、评论、热度更新。
- 能说明摄影师如何发布、编辑、上下架自己的作品。
- 能说明作品图片上传流程。

### 成员 C

- 能说明用户、摄影师两张表的关系。
- 能说明摄影师认证状态。
- 能说明个人中心展示哪些数据。
- 能说明资料编辑弹窗和后端接口关系。

### 成员 D

- 能说明论坛板块和帖子表关系。
- 能说明帖子列表排序和帖子数统计。
- 能说明发帖、编辑、我的帖子。
- 能说明帖子评论数和点赞数维护。

### 成员 E

- 能说明后台控制台统计数据来源。
- 能说明公告、轮播、分类管理。
- 能说明系统日志怎么记录。
- 能说明后台权限如何限制普通用户访问。
