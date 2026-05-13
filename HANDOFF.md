# 摄影作品分享平台交接文档

## 新会话提示词

你现在接手一个 Flask 课程项目，项目是“摄影作品分享平台”。请先读取当前真实项目目录下的关键文件，不要把早期规划目录当成实现目录。

真实实现目录：

```text
D:\Program Files\Code\PyCharm\photo-manage-platform
```

优先读取：

- `HANDOFF.md`
- `README.md`
- `app.py`
- `config.py`
- `db.py`
- `models/*.py`
- `views/*.py`
- `templates/**/*.html`
- `utils/*.py`
- `photo_manage_platform.sql`

## 当前技术栈

- Python
- Flask
- SQLAlchemy
- Flask-Login
- MySQL
- Bootstrap
- 阿里云 OSS

## 当前实现状态

- 项目已接入真实 MySQL + SQLAlchemy + Flask-Login。
- 首页 `/` 已从数据库读取轮播图、精选作品、热门作品、最新作品、推荐摄影师。
- 登录入口已统一为 `/auth/login`：
  - 普通用户和管理员共用一个登录页面。
  - 自动识别逻辑为先查普通用户，再查管理员。
  - 普通用户登录后进入首页。
  - 管理员登录后进入 `/admin/dashboard/`。
  - 旧 `/auth/admin_login` 保留兼容，访问会重定向到 `/auth/login`。
- 管理员登录态访问首页 `/` 或登录页 `/auth/login` 会自动跳转后台控制台，避免显示成普通用户界面。
- 前台导航已区分普通用户和管理员：
  - 普通用户显示用户中心和退出。
  - 管理员显示后台控制台和退出。
- 密码方案仍是 MD5。
  - 新注册和改密写入 MD5。
  - 旧明文密码兼容迁移仍保留，登录成功后自动升级为 MD5。
- 本地数据库中已验证可登录的账号：
  - `admin / 123456`
  - `user1 / 123456`
  - `user2 / 123456`
  - `user3 / 123456`
  - `user_test / 123456`
- 图片上传已接入阿里云 OSS：
  - 流程为先保存本地 `static/uploads/<module>/`，再上传 OSS。
  - 数据库保存 OSS URL。
  - OSS 成功后保留本地副本。
  - OSS 上传失败会删除本次新保存的本地文件并中止保存。
- 轮播图后台上传已接入首页展示。

## OSS 配置与行为

`config.py` 从环境变量读取 OSS 密钥，不再硬编码 AccessKey：

```powershell
$env:OSS_ACCESS_KEY_ID="你的 AccessKey ID"
$env:OSS_ACCESS_KEY_SECRET="你的 AccessKey Secret"
$env:OSS_ENDPOINT="oss-cn-wuhan-lr.aliyuncs.com"
$env:OSS_BUCKET_NAME="photo-manage-oss"
$env:OSS_UPLOAD_PREFIX="photo-manage-platform"
$env:OSS_BUCKET_DOMAIN="photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com"
python app.py
```

当前 OSS 连通性已验证：

- 能上传测试对象。
- 能删除测试对象。
- 生成 URL 格式正确。

注意：AccessKey 不应写入仓库文件。如果环境变量变更，需要重启 Flask/PyCharm 运行进程。若旧密钥已经暴露给不可信环境，应在阿里云控制台禁用或轮换。

## 业务规则

- 不需要收藏功能。
- 不存在 `work_favorite` 表。
- 不要重新引入 `favorite`、`work_favorite`、收藏相关功能。
- 当前保留的是作品点赞 `work_like`。
- `photographer` 摄影师认证资料不包含“摄影师简介”和“从业年限”。
- `category` 分类表不包含“分类描述”。
- `photo_work` 作品表不包含“收藏数”。
- 外键、可空和删除级联策略应与 `photo_manage_platform.sql` 保持一致。
- 后台路由使用 `/admin/<module>/...`。
- 前台路由使用 `/work/...`、`/photographer/...`、`/forum/...`、`/announcement/...`。
- 作品互动 API 使用 `/api/work/<work_id>/like` 和 `/api/work/<work_id>/comment`。

## 主要文件说明

- `app.py`：Flask 入口，初始化数据库、登录管理、蓝图和首页查询。
- `config.py`：数据库、Flask、OSS 配置。
- `db.py`：SQLAlchemy 实例。
- `views/auth.py`：统一登录、注册、登出、用户加载。
- `utils/encryption.py`：MD5 和旧明文兼容。
- `utils/decorators.py`：普通用户/管理员权限装饰器。
- `utils/file_upload.py`：统一图片上传入口，本地 + OSS。
- `utils/oss_utils.py`：OSS bucket、上传、删除、URL/object key 工具。
- `models/*.py`：SQLAlchemy 模型。
- `templates/**/*.html`：页面模板。

## 后续建议

- 模板中仍有部分历史中文乱码，后续如果修 UI 文案，应逐个模板检查，不要盲目全量替换。
- 如果要交付可复现数据库，应补充初始化数据脚本，并确保密码为 MD5。
- OSS AccessKey 已改为环境变量读取，不要重新硬编码到 `config.py` 或其他仓库文件。
- 每次修改后至少运行编译、导入和核心路由检查。
