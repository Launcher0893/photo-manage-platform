# 摄影作品分享平台项目结构与开发计划

## 1. 项目概述

摄影作品分享平台是一个基于 Flask 的 Web 项目，面向普通用户、摄影师和管理员三类角色。普通用户可以浏览摄影作品、搜索摄影师、点赞评论、在论坛发帖交流；摄影师可以展示个人资料和作品集；管理员可以在后台管理作品、摄影师认证、用户、论坛、评论、公告、首页轮播图，并通过图表查看平台运营数据。

本项目参考老师提供的小说管理系统项目结构和阿里云 OSS 上传示例，但业务内容全部改为摄影作品分享平台。

## 2. 技术栈

| 类型 | 技术 |
| --- | --- |
| 核心语言 | Python |
| Web 框架 | Flask |
| 前端技术 | HTML5、CSS、JavaScript |
| 前端框架 | Bootstrap、jQuery、Layer |
| 图表工具 | ECharts |
| 数据库 | MySQL |
| ORM | Flask-SQLAlchemy |
| 登录状态管理 | Flask-Login |
| 数据库管理工具 | Navicat |
| 文件存储 | 阿里云 OSS |
| 版本控制 | Git |

## 3. 项目目录结构设计

```text
photo_manage_platform/
├── app.py                         # Flask 项目入口，注册蓝图和初始化扩展
├── config.py                      # 数据库、OSS、上传目录、分页等配置
├── db.py                          # SQLAlchemy 数据库对象
├── requirements.txt               # Python 依赖包
├── photo_manage_platform.sql      # 后续导出的数据库 SQL 文件
├── photography-platform-design-plan.md
├── models/                        # 数据库模型
│   ├── Admin.py
│   ├── Role.py
│   ├── User.py
│   ├── Photographer.py
│   ├── Category.py
│   ├── PhotoWork.py
│   ├── PhotoWorkImage.py
│   ├── WorkLike.py
│   ├── WorkComment.py
│   ├── ForumBoard.py
│   ├── ForumPost.py
│   ├── ForumPostImage.py
│   ├── ForumComment.py
│   ├── Announcement.py
│   ├── Carousel.py
│   └── SystemLog.py
├── views/                         # 蓝图路由
│   ├── auth.py                    # 用户/管理员登录注册
│   ├── dashboard.py               # 后台首页与统计图表
│   ├── user.py                    # 用户管理与个人中心
│   ├── photographer.py            # 摄影师管理与摄影师主页
│   ├── work.py                    # 作品管理与用户端作品展示
│   ├── category.py                # 分类与标签管理
│   ├── forum.py                   # 论坛板块、帖子、评论
│   ├── announcement.py            # 公告管理与公告展示
│   ├── carousel.py                # 首页轮播图管理
│   └── api.py                     # 图表数据、点赞等 Ajax 接口
├── utils/                         # 工具函数
│   ├── encryption.py              # MD5 密码加密
│   ├── oss_utils.py               # 阿里云 OSS 上传、删除、URL 生成
│   ├── file_upload.py             # 文件后缀校验、文件名生成、上传封装
│   ├── decorators.py              # 登录和权限校验装饰器
│   ├── pagination.py              # 分页工具
│   └── logger.py                  # 系统操作日志记录
├── templates/                     # HTML 模板
│   ├── base.html                  # 用户端公共布局
│   ├── admin_base.html            # 管理后台公共布局
│   ├── index.html                 # 用户端首页
│   ├── login.html
│   ├── register.html
│   ├── admin_login.html
│   ├── dashboard/
│   ├── user/
│   ├── photographer/
│   ├── work/
│   ├── category/
│   ├── forum/
│   ├── announcement/
│   └── carousel/
└── static/
    ├── css/
    ├── js/
    ├── bootstrap/
    ├── jquery/
    ├── layer/
    ├── echarts/
    └── uploads/                  # 本地临时上传目录，正式图片以 OSS URL 为准
```

## 4. 核心功能实现方案

### 4.1 登录注册模块

用户端提供注册、登录、退出功能。注册时用户输入用户名、密码和角色，角色可选择普通用户或摄影师。普通用户注册后只写入 `user` 表；摄影师注册后同时写入 `user` 表和 `photographer` 表，并将摄影师认证状态设置为待审核。

管理员使用独立登录入口，登录信息来自 `admin` 表。普通用户和管理员登录逻辑分开，避免普通用户访问后台管理页面。

密码按需求使用 MD5 加密后存入数据库。实现时在 `utils/encryption.py` 中封装 `md5_encrypt(password)` 方法，注册和登录验证时都调用同一个方法。

### 4.2 用户端首页

首页展示轮播图、精选摄影作品、推荐摄影师和热门作品。最新已发布公告以弹窗形式展示，顶部导航保留公告列表入口。

轮播图数据来自 `carousel` 表；精选作品来自 `photo_work.is_featured = 1` 且审核通过、上架的作品；推荐摄影师来自审核通过且用户状态正常的摄影师资料；公告来自 `announcement` 表中已发布的数据。首页只主动弹出最新一条公告，用户勾选“不再弹出此公告”后通过浏览器 `localStorage` 记录隐藏状态；未勾选时下次进入首页仍继续弹出。

### 4.3 作品浏览与搜索

用户可以查看作品列表，并通过关键词、分类、城市、热度、发布时间进行筛选和排序。

作品列表主要查询 `photo_work` 表，并关联 `photographer`、`user`、`category` 表显示摄影师昵称、风格分类等信息。作品详情页展示标题、摄影师、拍摄城市、作品描述、组图轮播、浏览量、点赞数和评论区。

进入作品详情页时，后端将 `view_count` 加 1，并重新计算热度分。

### 4.4 作品点赞和评论

点赞使用 `work_like` 表记录用户和作品的关系。每个用户对同一个作品只能点赞一次，因此需要给 `work_id + user_id` 建唯一约束。

评论写入 `work_comment` 表。普通用户提交评论后默认显示，也可以按项目要求设置为待审核。管理员后台可以查看、删除或禁用评论。

作品热度分建议按以下公式计算：

```text
hot_score = view_count + like_count * 3 + comment_count * 2
```

### 4.5 摄影师模块

摄影师信息拆分为 `user` 表和 `photographer` 表。`user` 表保存登录账号、昵称、头像等基础信息；`photographer` 表保存真实姓名、所在城市、认证状态等摄影师资料。

摄影师注册后进入待审核状态。管理员审核通过且用户状态正常后，该摄影师才可以被展示在用户端推荐摄影师列表中。摄影师主页自动聚合该摄影师发布或由管理员维护的所有公开作品。

### 4.6 管理后台控制台

后台首页展示平台核心数据：

- 总作品数
- 总用户数
- 审核通过的摄影师数
- 待审核摄影师数
- 最近 7 天新增用户与新增作品趋势图
- 热门作品 Top 10
- 作品分类占比饼图

图表接口放在 `views/api.py` 或 `views/dashboard.py` 中，前端通过 Ajax 获取 JSON 数据，使用 ECharts 渲染。

### 4.7 作品管理

管理员可以新增、编辑、删除、审核和下架作品。新增作品时选择摄影师、分类、拍摄城市，填写标题和描述，并上传封面图和作品组图。

封面图 URL 存入 `photo_work.cover_url`；组图每张图片单独写入 `photo_work_image` 表。图片上传流程为：前端表单提交文件，后端校验后缀和大小，生成唯一文件名，调用 OSS 工具上传，上传成功后将 OSS URL 写入数据库。

审核通过的摄影师也可以在前台自行发布、编辑、下架和恢复自己的作品。摄影师发布作品默认审核通过并上架，但不能设置首页精选，也不能选择或修改其他摄影师名下的作品。

### 4.8 分类与标签管理

分类与标签统一使用 `category` 表。管理员可以新增、编辑、删除或禁用分类，例如日系小清新、复古胶片、黑白光影、森系、ins 风、情绪片。

作品通过 `photo_work.category_id` 关联分类。后续如需要一个作品拥有多个标签，可以扩展中间表 `work_category`，第一版先采用一个作品对应一个主分类，降低实现难度。

### 4.9 用户管理

管理员可以查看用户列表，按用户名、昵称、角色、状态筛选用户。管理员可以启用、禁用、软删除和恢复用户，查看用户详情和注册时间。软删除使用 `user.status = -1`，用户列表默认隐藏已删除用户，需通过状态筛选查看和恢复。

个人中心支持用户修改头像、修改密码、查看我的帖子。审核通过的摄影师进入个人中心时默认展示“我的作品”，并提供发布作品、管理作品入口。头像上传到 OSS，返回的 URL 存入 `user.avatar_url`。

### 4.10 论坛模块

论坛包含板块、帖子、帖子图片、帖子评论。板块由管理员维护，例如作品交流、技巧分享。

用户发帖时选择板块，填写标题和内容，可上传多张图片。帖子图片上传到 OSS 后写入 `forum_post_image` 表。帖子详情页展示内容、图片、点赞数、浏览量和评论。

管理员可以删除帖子、删除评论、置顶帖子。置顶通过 `forum_post.is_top` 字段控制。

### 4.11 公告与轮播图管理

公告由管理员发布，支持标题、内容和封面图片。公告图片上传到 OSS，图片地址存入 `announcement.cover_url`。

轮播图由管理员配置，支持图片、标题、跳转类型、跳转目标和排序。跳转类型可以是作品、摄影师、公告或外部链接。

### 4.12 阿里云 OSS 上传方案

OSS 配置放在 `config.py` 中，正式开发时建议通过环境变量读取，不要把密钥写死到代码仓库中。

```python
OSS_ACCESS_KEY_ID = os.environ.get('OSS_ACCESS_KEY_ID')
OSS_ACCESS_KEY_SECRET = os.environ.get('OSS_ACCESS_KEY_SECRET')
OSS_ENDPOINT = os.environ.get('OSS_ENDPOINT')
OSS_BUCKET_NAME = os.environ.get('OSS_BUCKET_NAME')
```

统一上传方法建议放在 `utils/oss_utils.py`：

```text
upload_to_oss(file, folder) -> { url, object_name }
delete_from_oss(object_name) -> bool
```

不同业务使用不同 OSS 目录：

| 业务 | OSS 目录 |
| --- | --- |
| 用户头像 | avatars/ |
| 摄影师头像 | avatars/ |
| 作品封面 | works/covers/ |
| 作品组图 | works/images/ |
| 论坛图片 | forum/posts/ |
| 公告图片 | announcements/ |
| 轮播图 | carousels/ |

## 5. 数据库设计

数据库名称建议为 `photo_manage_platform`，字符集使用 `utf8mb4`，存储引擎使用 `InnoDB`。

### 5.1 role 管理员角色表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| role_id | int | PK, AI | 角色 ID |
| role_name | varchar(30) | not null | 角色名称 |
| permissions | varchar(255) | null | 权限标识 |
| remark | varchar(100) | null | 备注 |
| create_time | datetime | default CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | default CURRENT_TIMESTAMP | 更新时间 |

### 5.2 admin 管理员表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| admin_id | int | PK, AI | 管理员 ID |
| admin_account | varchar(50) | unique, not null | 登录账号 |
| admin_password | varchar(100) | not null | 登录密码，MD5 加密 |
| admin_name | varchar(30) | not null | 管理员姓名 |
| role_id | int | FK | 关联 `role.role_id` |
| status | smallint | default 1 | 状态：1 正常，0 禁用 |
| create_time | datetime | default CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | default CURRENT_TIMESTAMP | 更新时间 |

关系：一个角色可以对应多个管理员，`role 1:N admin`。

### 5.3 user 用户表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| user_id | int | PK, AI | 用户 ID |
| username | varchar(50) | unique, not null | 登录用户名 |
| password | varchar(100) | not null | 登录密码，MD5 加密 |
| nickname | varchar(30) | null | 昵称 |
| email | varchar(100) | null | 邮箱 |
| phone | varchar(20) | null | 手机号 |
| avatar_url | varchar(255) | null | 头像 OSS 地址 |
| user_role | smallint | default 1 | 角色：1 普通用户，2 摄影师 |
| status | smallint | default 1 | 状态：1 正常，0 禁用 |
| create_time | datetime | default CURRENT_TIMESTAMP | 注册时间 |
| update_time | datetime | default CURRENT_TIMESTAMP | 更新时间 |

### 5.4 photographer 摄影师认证资料表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| photographer_id | int | PK, AI | 摄影师 ID |
| user_id | int | FK, unique | 关联 `user.user_id` |
| real_name | varchar(30) | null | 真实姓名 |
| city | varchar(50) | null | 所在城市 |
| cert_status | smallint | default 0 | 认证状态：0 待审核，1 通过，2 拒绝 |
| cert_remark | varchar(255) | null | 审核备注 |
| audit_admin_id | int | FK, null | 审核管理员 |
| audit_time | datetime | null | 审核时间 |
| create_time | datetime | default CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | default CURRENT_TIMESTAMP | 更新时间 |

关系：一个用户最多对应一个摄影师资料，`user 1:1 photographer`。

### 5.5 category 作品分类/风格标签表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| category_id | int | PK, AI | 分类 ID |
| category_name | varchar(50) | unique, not null | 分类名称 |
| sort | int | default 0 | 排序值 |
| status | smallint | default 1 | 状态：1 启用，0 禁用 |
| create_time | datetime | default CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | default CURRENT_TIMESTAMP | 更新时间 |

### 5.6 photo_work 摄影作品表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| work_id | int | PK, AI | 作品 ID |
| title | varchar(100) | not null | 作品标题 |
| photographer_id | int | FK | 摄影师 ID |
| category_id | int | FK | 分类 ID |
| cover_url | varchar(255) | null | 封面图 OSS 地址 |
| city | varchar(50) | null | 拍摄城市 |
| description | text | null | 作品描述 |
| view_count | int | default 0 | 浏览量 |
| like_count | int | default 0 | 点赞数 |
| comment_count | int | default 0 | 评论数 |
| hot_score | int | default 0 | 热度分 |
| audit_status | smallint | default 0 | 审核状态：0 待审核，1 通过，2 拒绝 |
| is_featured | smallint | default 0 | 是否精选：1 是，0 否 |
| status | smallint | default 1 | 状态：1 上架，0 下架 |
| create_time | datetime | default CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | default CURRENT_TIMESTAMP | 更新时间 |

关系：一个摄影师可以有多个作品，`photographer 1:N photo_work`；一个分类可以有多个作品，`category 1:N photo_work`。

### 5.7 photo_work_image 作品组图表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| image_id | int | PK, AI | 图片 ID |
| work_id | int | FK | 作品 ID |
| image_url | varchar(255) | not null | 图片 OSS 地址 |
| oss_object_name | varchar(255) | null | OSS 文件对象名，用于删除 |
| sort | int | default 0 | 排序值 |
| create_time | datetime | default CURRENT_TIMESTAMP | 创建时间 |

关系：一个作品可以有多张组图，`photo_work 1:N photo_work_image`。

### 5.8 work_like 作品点赞表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| like_id | int | PK, AI | 点赞 ID |
| work_id | int | FK | 作品 ID |
| user_id | int | FK | 用户 ID |
| create_time | datetime | default CURRENT_TIMESTAMP | 点赞时间 |

约束：`work_id + user_id` 建唯一索引，防止重复点赞。

### 5.9 work_comment 作品评论表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| comment_id | int | PK, AI | 评论 ID |
| work_id | int | FK | 作品 ID |
| user_id | int | FK | 评论用户 ID |
| content | text | not null | 评论内容 |
| audit_status | smallint | default 1 | 审核状态：0 待审核，1 通过，2 拒绝 |
| status | smallint | default 1 | 状态：1 正常，0 删除 |
| create_time | datetime | default CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | default CURRENT_TIMESTAMP | 更新时间 |

关系：一个作品可以有多条评论，`photo_work 1:N work_comment`；一个用户可以发表多条评论，`user 1:N work_comment`。

### 5.10 forum_board 论坛板块表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| board_id | int | PK, AI | 板块 ID |
| board_name | varchar(50) | unique, not null | 板块名称 |
| description | varchar(255) | null | 板块描述 |
| sort | int | default 0 | 排序值 |
| status | smallint | default 1 | 状态：1 启用，0 禁用 |
| create_time | datetime | default CURRENT_TIMESTAMP | 创建时间 |

### 5.11 forum_post 论坛帖子表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| post_id | int | PK, AI | 帖子 ID |
| board_id | int | FK | 所属板块 ID |
| user_id | int | FK | 发帖用户 ID |
| title | varchar(100) | not null | 帖子标题 |
| content | text | not null | 帖子内容 |
| view_count | int | default 0 | 浏览量 |
| like_count | int | default 0 | 点赞数 |
| comment_count | int | default 0 | 评论数 |
| is_top | smallint | default 0 | 是否置顶：1 是，0 否 |
| status | smallint | default 1 | 状态：1 正常，0 删除 |
| create_time | datetime | default CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | default CURRENT_TIMESTAMP | 更新时间 |

关系：一个论坛板块可以有多个帖子，`forum_board 1:N forum_post`。

### 5.12 forum_post_image 帖子图片表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| image_id | int | PK, AI | 图片 ID |
| post_id | int | FK | 帖子 ID |
| image_url | varchar(255) | not null | 图片 OSS 地址 |
| oss_object_name | varchar(255) | null | OSS 文件对象名 |
| sort | int | default 0 | 排序值 |
| create_time | datetime | default CURRENT_TIMESTAMP | 创建时间 |

### 5.13 forum_comment 帖子评论表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| comment_id | int | PK, AI | 评论 ID |
| post_id | int | FK | 帖子 ID |
| user_id | int | FK | 评论用户 ID |
| content | text | not null | 评论内容 |
| status | smallint | default 1 | 状态：1 正常，0 删除 |
| create_time | datetime | default CURRENT_TIMESTAMP | 创建时间 |

关系：一个帖子可以有多条评论，`forum_post 1:N forum_comment`。

### 5.14 announcement 公告表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| announcement_id | int | PK, AI | 公告 ID |
| title | varchar(100) | not null | 公告标题 |
| content | text | not null | 公告内容 |
| cover_url | varchar(255) | null | 公告图片 OSS 地址 |
| admin_id | int | FK | 发布管理员 |
| status | smallint | default 1 | 状态：1 发布，0 下架 |
| create_time | datetime | default CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | default CURRENT_TIMESTAMP | 更新时间 |

### 5.15 carousel 首页轮播图表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| carousel_id | int | PK, AI | 轮播图 ID |
| title | varchar(100) | null | 轮播标题 |
| image_url | varchar(255) | not null | 图片 OSS 地址 |
| link_type | varchar(30) | null | 跳转类型：work、photographer、announcement、url |
| link_id | int | null | 跳转目标 ID |
| link_url | varchar(255) | null | 外部跳转地址 |
| sort | int | default 0 | 排序值 |
| status | smallint | default 1 | 状态：1 启用，0 禁用 |
| create_time | datetime | default CURRENT_TIMESTAMP | 创建时间 |

### 5.16 system_log 系统操作日志表

| 字段 | 类型 | 约束 | 说明 |
| --- | --- | --- | --- |
| log_id | int | PK, AI | 日志 ID |
| admin_id | int | FK | 操作管理员 |
| operate_type | varchar(30) | not null | 操作类型 |
| operate_content | varchar(255) | not null | 操作内容 |
| ip_address | varchar(50) | null | 操作 IP |
| operate_time | datetime | default CURRENT_TIMESTAMP | 操作时间 |

## 6. 数据库关系汇总

| 关系 | 说明 |
| --- | --- |
| role 1:N admin | 一个角色可以分配给多个管理员 |
| user 1:1 photographer | 一个用户最多拥有一份摄影师认证资料 |
| admin 1:N photographer | 一个管理员可以审核多个摄影师 |
| photographer 1:N photo_work | 一个摄影师可以拥有多个摄影作品 |
| category 1:N photo_work | 一个分类下可以有多个作品 |
| photo_work 1:N photo_work_image | 一个作品可以有多张组图 |
| photo_work 1:N work_comment | 一个作品可以有多条评论 |
| photo_work N:N user | 通过 `work_like` 实现用户点赞作品 |
| forum_board 1:N forum_post | 一个板块可以有多个帖子 |
| forum_post 1:N forum_post_image | 一个帖子可以有多张图片 |
| forum_post 1:N forum_comment | 一个帖子可以有多条评论 |
| admin 1:N announcement | 一个管理员可以发布多条公告 |
| admin 1:N system_log | 一个管理员可以产生多条操作日志 |

## 7. 后端蓝图设计

| 蓝图 | URL 前缀 | 主要功能 |
| --- | --- | --- |
| auth | `/auth` | 用户登录、注册、退出、管理员登录 |
| dashboard | `/admin/dashboard` | 后台首页、统计卡片、图表页面 |
| user | `/admin/user`、`/user` | 后台用户管理、用户个人中心 |
| photographer | `/photographer`、`/admin/photographer` | 摄影师展示、摄影师审核 |
| work | `/work`、`/admin/work` | 用户端作品展示、后台作品管理 |
| category | `/admin/category` | 分类标签管理 |
| forum | `/forum`、`/admin/forum` | 论坛帖子、评论、后台论坛管理 |
| announcement | `/announcement`、`/admin/announcement` | 公告展示和公告管理 |
| carousel | `/admin/carousel` | 首页轮播图管理 |
| api | `/api` | 点赞、图表数据等 Ajax 接口 |

## 8. 页面设计

### 8.1 用户端页面

| 页面 | 文件 |
| --- | --- |
| 首页 | `templates/index.html` |
| 用户登录 | `templates/login.html` |
| 用户注册 | `templates/register.html` |
| 作品列表 | `templates/work/list.html` |
| 作品详情 | `templates/work/detail.html` |
| 摄影师列表 | `templates/photographer/list.html` |
| 摄影师主页 | `templates/photographer/detail.html` |
| 论坛板块 | `templates/forum/board.html` |
| 帖子列表 | `templates/forum/post_list.html` |
| 帖子详情 | `templates/forum/post_detail.html` |
| 发布帖子 | `templates/forum/post_add.html` |
| 个人中心 | `templates/user/profile.html` |

### 8.2 管理后台页面

| 页面 | 文件 |
| --- | --- |
| 管理员登录 | `templates/admin_login.html` |
| 后台首页 | `templates/dashboard/index.html` |
| 作品列表 | `templates/work/admin_list.html` |
| 作品新增/编辑 | `templates/work/admin_form.html` |
| 摄影师审核 | `templates/photographer/admin_list.html` |
| 分类管理 | `templates/category/list.html` |
| 用户管理 | `templates/user/admin_list.html` |
| 论坛管理 | `templates/forum/admin_post_list.html` |
| 评论管理 | `templates/forum/admin_comment_list.html` |
| 公告管理 | `templates/announcement/admin_list.html` |
| 轮播图管理 | `templates/carousel/list.html` |
| 系统日志 | `templates/system/log_list.html` |

## 9. 五人协作分工表

| 成员 | 负责方向 | 主要任务 | 交付内容 |
| --- | --- | --- | --- |
| 成员 1 | 项目基础与登录权限 | 搭建 Flask 项目结构，配置数据库连接，完成用户注册、用户登录、管理员登录、退出登录、MD5 密码加密和后台权限控制 | `app.py`、`config.py`、`db.py`、`views/auth.py`、登录注册相关模板 |
| 成员 2 | 数据库与后台基础管理 | 设计并创建 MySQL 数据表，完成用户管理、摄影师审核、分类管理、系统日志记录 | 数据库 SQL、`models/` 基础模型、用户/摄影师/分类后台页面 |
| 成员 3 | 摄影作品模块 | 完成作品新增、编辑、删除、审核、下架、作品组图管理、作品列表搜索、作品详情、点赞和评论功能 | 作品相关模型、`views/work.py`、作品后台和用户端页面 |
| 成员 4 | 论坛与公告模块 | 完成论坛板块、发帖、帖子图片、帖子评论、删帖、置顶、公告管理和轮播图管理 | 论坛/公告/轮播相关模型、路由和模板 |
| 成员 5 | OSS 上传与数据可视化 | 封装阿里云 OSS 上传工具，接入头像、作品图、帖子图、公告图上传；完成后台统计卡片和 ECharts 图表 | `utils/oss_utils.py`、`utils/file_upload.py`、图表接口、后台控制台页面 |

协作要求：

1. 每个成员只修改自己负责的模块，公共文件如 `app.py`、`config.py`、`admin_base.html` 修改前需要先沟通。
2. 数据库字段变更必须同步更新 SQL、模型类和相关页面表单。
3. 每完成一个模块至少提交一次 Git commit，提交信息说明清楚完成的功能。
4. 合并代码前需要运行项目并验证自己负责页面可以正常访问。
5. OSS 密钥不允许提交到 Git 仓库，只能放在本地配置或环境变量中。

## 10. 开发阶段计划

### 第一阶段：项目基础搭建

1. 创建 Flask 项目基础目录。
2. 配置 `config.py`、`db.py`、`app.py`。
3. 安装 Flask、Flask-SQLAlchemy、PyMySQL、Flask-Login、oss2 等依赖。
4. 创建 MySQL 数据库 `photo_manage_platform`。
5. 编写模型类并通过 Navicat 或 SQL 脚本创建数据表。

### 第二阶段：登录注册与权限

1. 完成普通用户注册、摄影师注册。
2. 完成普通用户登录和退出。
3. 完成管理员独立登录。
4. 增加后台访问权限控制。
5. 实现 MD5 密码加密。

### 第三阶段：后台基础管理

1. 实现用户管理。
2. 实现摄影师认证审核。
3. 实现分类标签管理。
4. 实现作品新增、编辑、删除、审核、下架。
5. 实现公告和轮播图管理。

### 第四阶段：用户端核心功能

1. 实现首页数据展示。
2. 实现作品列表、搜索、筛选和详情页。
3. 实现点赞和作品评论。
4. 实现摄影师列表和摄影师主页。
5. 实现个人中心。

### 第五阶段：论坛与 OSS 上传

1. 实现论坛板块、帖子发布、帖子详情和帖子评论。
2. 接入阿里云 OSS 上传工具。
3. 完成头像、作品组图、帖子图片、公告图片、轮播图上传。
4. 保存 OSS URL 和 object name 到数据库。

### 第六阶段：数据可视化与测试

1. 实现后台统计卡片。
2. 实现最近 7 天新增用户和作品趋势图。
3. 实现作品分类占比饼图。
4. 实现热门作品 Top 10。
5. 完成主要功能测试和演示数据准备。

## 11. 测试与验收标准

| 测试项 | 验收标准 |
| --- | --- |
| 用户注册登录 | 普通用户和摄影师可以注册登录，密码加密后入库 |
| 管理员登录 | 管理员可进入后台，普通用户不能进入后台 |
| 摄影师审核 | 摄影师注册后待审核，管理员审核通过后可在用户端展示 |
| 作品管理 | 管理员可以新增、编辑、删除、审核作品；摄影师可以管理自己名下作品 |
| OSS 上传 | 头像、作品图片、帖子图片、公告图片上传后可正常访问 |
| 重复提交防护 | 上传或保存表单提交后按钮禁用，重复点击不会产生多条相同数据 |
| 作品互动 | 用户可以点赞、评论作品，重复点赞被限制 |
| 论坛功能 | 用户可以发帖、评论，管理员可以删帖、删评论、置顶 |
| 公告弹窗 | 首页弹出最新公告；勾选不再弹出后同一公告不再主动弹出，未勾选则每次进入首页弹出 |
| 用户软删除 | 后台可软删除和恢复用户，已删除用户默认不在列表显示，禁用或删除摄影师后前台隐藏其公开内容 |
| 搜索分页 | 作品、摄影师、帖子、后台列表支持关键词搜索和分页 |
| 可视化图表 | 图表数据与数据库统计结果一致 |
| 系统日志 | 管理员关键操作可以写入日志表 |

## 12. 关键实现注意事项

1. OSS 密钥不能提交到 Git 仓库，正式项目应使用环境变量或 `.env` 文件管理；`.env.example` 只保留占位示例。
2. 上传文件必须限制后缀和大小，只允许 `jpg`、`jpeg`、`png`、`gif`、`webp` 等图片格式。
3. 删除数据库图片记录时，如果有 `oss_object_name`，应同步调用 OSS 删除方法。
4. 用户端和后台端模板要分开，避免权限和页面逻辑混乱。
5. 作品点赞数、评论数可以在新增或删除互动记录时同步更新到 `photo_work` 表，方便列表页排序。
6. 数据库表统一使用 `create_time`、`update_time`、`status` 字段，方便管理和筛选。
7. 后台删除建议优先使用软删除。普通启用/禁用使用 `status = 1/0`，用户删除使用 `status = -1`，避免误删重要数据。
8. 第一版按课程项目难度设计为 Flask 服务端渲染，不做前后端分离。

## 13. 后续可扩展功能

1. 作品支持多个标签，新增 `work_category` 中间表。
2. 评论增加回复功能，支持楼中楼。
3. 用户关注摄影师，新增 `photographer_follow` 表。
4. 后台增加更细的角色权限控制。
5. 首页推荐作品根据热度和分类自动计算。
6. 增加图片压缩、水印和缩略图生成。
