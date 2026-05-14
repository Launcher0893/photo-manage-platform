# 摄影作品分享平台交接文档

## 新会话提示词

你现在接手一个 Flask 课程项目，项目是“摄影作品分享平台”，请先读取当前真实项目目录下的关键文件。

- `HANDOFF.md`
- `README.md`
- `photography-platform-design-plan.md`
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
- Flask-WTF
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
- 登录表单使用 POST 提交，GET `/auth/login` 只用于渲染页面。
- 项目已启用 Flask-WTF CSRF 防护：
  - `app.py` 初始化 `CSRFProtect`。
  - 基础模板提供 `csrf-token` meta。
  - 常规 POST 表单已加入 `csrf_token`。
  - Ajax 请求通过 `X-CSRFToken` 请求头提交。
- 前台导航已区分普通用户和管理员：
  - 普通用户昵称左侧有独立 `发布帖子` 入口 `/forum/post_add`。
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
- 项目已支持 `.env` 本地配置：
  - `config.py` 会在安装 `python-dotenv` 时自动读取根目录 `.env`。
  - 未安装 `python-dotenv` 时仍可使用系统环境变量。
  - `.env` 已被 `.gitignore` 忽略，真实密钥不要提交。
  - `.env.example` 是可提交的本地配置模板。
- 前台和后台基础模板已加入通用 POST 表单重复提交防护：
  - 表单提交后会记录 submitting 状态。
  - 提交按钮会禁用并显示 `处理中...`。
  - 主要用于避免上传图片时多次点击造成重复保存。
- 轮播图后台上传已接入首页展示。
- `photo_manage_platform.sql` 已恢复 3 条真实 OSS 轮播测试图数据：`test`、`test2`、`test3`。
- 首页精选作品来自 `photo_work.is_featured = 1` 且审核通过、上架的作品；精选状态由管理员在后台作品新增/编辑页维护，摄影师前台不能自设精选。
- 首页、作品列表/详情、摄影师列表/详情会过滤 `user.status != 1` 的摄影师用户，禁用或软删除摄影师后前台不再展示其相关公开内容。
- 首页公告已改为弹窗：
  - 首页 `/` 读取最新一条已发布公告作为 `latest_announcement`。
  - 页面底部不再展示“最新公告”卡片。
  - 顶部导航 `公告` 入口仍指向 `/announcement/list`。
  - 只有用户勾选 `不再弹出此公告` 时，前端才写入 `localStorage` 的 `hiddenAnnouncement:<announcement_id>`。
  - 未勾选时，下次进入首页仍会弹出同一公告。
- 公告后台支持发布、编辑、上下架和删除；删除公告时会尝试同步清理封面图片。
- 论坛用户发帖已调整：
  - 独立发帖入口为 `/forum/post_add`。
  - 板块内发帖入口 `/forum/post_add/<board_id>` 保留，会默认选中当前板块。
  - 发帖表单使用板块下拉菜单，不再输入板块名。
  - 用户可通过 `/forum/post_edit/<post_id>` 编辑自己的帖子。
  - 编辑时支持修改标题、内容、所属板块，追加新图片，并删除旧图片。
  - 帖子详情页和个人中心会给作者显示编辑入口。
- 摄影师前台作品闭环已接入：
  - 摄影师用户可在个人中心查看认证状态，并通过 `/user/edit_photographer` 完善真实姓名和所在城市。
  - 审核通过后显示 `/work/add` 发布作品和 `/work/my` 我的作品入口。
  - 摄影师可编辑自己的作品 `/work/edit/<work_id>`，支持替换封面、追加组图、删除旧组图。
  - 摄影师可通过 `/work/status/<work_id>` 下架或恢复自己的作品。
  - 摄影师前台发布作品默认 `audit_status = 1`、`status = 1`，保存后直接在前台展示。
  - 摄影师只能管理自己名下作品，不能选择或修改其他摄影师的作品。
- 个人中心已调整：
  - 审核通过的摄影师默认直接展示“我的作品”。
  - “我的帖子”仍在个人中心下方展示。
- 后台用户管理已支持软删除：
  - `user.status = 1` 表示正常。
  - `user.status = 0` 表示禁用。
  - `user.status = -1` 表示已删除。
  - 用户列表默认隐藏已删除用户，可通过状态筛选查看。
  - 已删除用户可恢复，已删除状态不能直接启用或禁用。

## OSS 配置与行为

`config.py` 从 `.env` 或系统环境变量读取 OSS 密钥，不再硬编码 AccessKey：

```powershell
$env:OSS_ACCESS_KEY_ID="你的 AccessKey ID"
$env:OSS_ACCESS_KEY_SECRET="你的 AccessKey Secret"
$env:OSS_ENDPOINT="oss-cn-wuhan-lr.aliyuncs.com"
$env:OSS_BUCKET_NAME="photo-manage-oss"
$env:OSS_UPLOAD_PREFIX="photo-manage-platform"
$env:OSS_BUCKET_DOMAIN="photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com"
python app.py
```

`.env` 示例见 `.env.example`。如果只在 `.env` 中填写 AccessKey，不需要加引号；包含空格或特殊字符时再使用引号更稳妥。上传大小由 `MAX_IMAGE_SIZE` 控制，单位为字节。

当前 OSS 连通性已验证：

- 能上传测试对象。
- 能删除测试对象。
- 生成 URL 格式正确。

注意：AccessKey 不应写入仓库文件。如果 `.env` 或环境变量变更，需要重启 Flask/PyCharm 运行进程。若旧密钥已经暴露给不可信环境，应在阿里云控制台禁用或轮换。

## 业务规则

- 不需要收藏功能。
- 不存在 `work_favorite` 表。
- 不要重新引入 `favorite`、`work_favorite`、收藏相关功能。
- 当前保留的是作品点赞 `work_like`。
- `photographer` 摄影师认证资料不包含“摄影师简介”和“从业年限”。
- `category` 分类表不包含“分类描述”。
- `photo_work` 作品表不包含“收藏数”。
- 作品评论提交后默认通过，写入 `audit_status = 1`；后台作品评论管理只做启用/禁用，不做评论审核通过/拒绝操作。
- 摄影师自行上传作品已经完成，不要再把它当作待开发扩展项。
- 用户删除采用软删除，不做物理删除数据库记录。
- 外键、可空和删除级联策略应与 `photo_manage_platform.sql` 保持一致。
- 后台路由使用 `/admin/<module>/...`。
- 前台路由使用 `/work/...`、`/photographer/...`、`/forum/...`、`/announcement/...`。
- 作品互动 API 使用 `/api/work/<work_id>/like` 和 `/api/work/<work_id>/comment`。

## 主要文件说明

- `app.py`：Flask 入口，初始化数据库、登录管理、蓝图和首页查询。
- `config.py`：数据库、Flask、OSS 配置。
- `db.py`：SQLAlchemy 实例。
- `views/auth.py`：统一登录、注册、登出、用户加载。
- `views/forum.py`：论坛板块、帖子列表、发帖、帖子编辑、帖子详情和评论。
- `utils/encryption.py`：MD5 和旧明文兼容。
- `utils/decorators.py`：普通用户/管理员权限装饰器。
- `utils/file_upload.py`：统一图片上传入口，本地 + OSS。
- `utils/oss_utils.py`：OSS bucket、上传、删除、URL/object key 工具。
- `models/*.py`：SQLAlchemy 模型。
- `templates/**/*.html`：页面模板。

## 后续建议

- 编码/模板结论：`HANDOFF.md`、`README.md`、`templates/**/*.html` 和 `photo_manage_platform.sql` 已按 UTF-8 正常解码；此前看到的 `鎽勫奖`、`歿{...}`、`?/a>` 等主要是终端或工具输出链路的显示乱码，不是文件内容损坏。
- 已验证 38 个模板 Jinja 语法解析通过，Flask loader 加载/编译通过；如果后续终端再次显示乱码，应优先用 Python UTF-8 读取或浏览器响应验证，不要直接改文件编码或盲目全量替换文案。
- 可复现数据库以 `photo_manage_platform.sql` 为准；其中已包含基础演示数据、MD5 演示账号和 3 条轮播测试图。
- OSS AccessKey 已改为环境变量读取，不要重新硬编码到 `config.py` 或其他仓库文件。
- 如果运行时报 `No module named 'flask_wtf'`，在项目虚拟环境执行 `python -m pip install -r requirements.txt`。
- 每次修改后至少运行编译、导入和核心路由检查。
- 公告弹窗测试时，如果浏览器曾经勾选过“不再弹出此公告”，可在控制台执行以下代码清理隐藏记录：

```javascript
Object.keys(localStorage).filter(k => k.startsWith('hiddenAnnouncement:')).forEach(k => localStorage.removeItem(k))
```
