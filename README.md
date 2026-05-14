# photo-manage-platform

摄影作品分享平台 Flask 课程项目。

## 运行说明

- 当前真实项目目录：`D:\Program Files\Code\PyCharm\photo-manage-platform`
- 默认数据库：本机 MySQL `photo_manage_platform`
- 默认连接串在 `config.py` 中，可通过环境变量或 `.env` 文件中的 `DATABASE_URL` 覆盖
- 首次运行前需要先导入 `photo_manage_platform.sql`
- 本项目使用 Flask、SQLAlchemy、Flask-Login、Flask-WTF、MySQL、Bootstrap
- `photo_manage_platform.sql` 已包含基础演示数据，导入后可直接使用下方账号登录
- `photo_manage_platform.sql` 已包含 3 张 OSS 轮播测试图数据，重导数据库后首页轮播不会丢失

启动：

```powershell
cd "D:\Program Files\Code\PyCharm\photo-manage-platform"
python -m pip install -r requirements.txt
python app.py
```

导入数据库示例：

```powershell
& 'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe' -uroot -p你的密码 --default-character-set=utf8mb4 photo_manage_platform --execute="source D:/Program Files/Code/PyCharm/photo-manage-platform/photo_manage_platform.sql"
```

## 本地配置 `.env`

项目已支持在根目录放置 `.env` 文件读取本地配置。依赖来自 `requirements.txt` 中的 `python-dotenv`；如果没有安装该依赖，项目仍会退回读取系统环境变量。

建议先参考 `.env.example` 创建自己的 `.env`，再按本机 MySQL 密码和 OSS 信息修改：

```env
SECRET_KEY=photo-manage-platform-dev-key
DATABASE_URL=mysql+pymysql://root:your_password@127.0.0.1:3306/photo_manage_platform?charset=utf8mb4
MAX_IMAGE_SIZE=20971520
OSS_ENABLED=true
OSS_ACCESS_KEY_ID=your_access_key_id
OSS_ACCESS_KEY_SECRET=your_access_key_secret
OSS_ENDPOINT=oss-cn-wuhan-lr.aliyuncs.com
OSS_BUCKET_NAME=photo-manage-oss
OSS_UPLOAD_PREFIX=photo-manage-platform
OSS_BUCKET_DOMAIN=photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com
```

`.env` 已在 `.gitignore` 中忽略，不要提交真实数据库密码或 OSS AccessKey。修改 `.env` 后需要重启 Flask/PyCharm 运行进程才会生效。

## 登录入口

- 统一登录入口：`/auth/login`
- 普通用户和管理员都在同一个页面输入账号和密码
- 登录逻辑先识别普通用户，再识别管理员
- 管理员登录成功后进入 `/admin/dashboard/`
- 旧入口 `/auth/admin_login` 保留兼容，会重定向到 `/auth/login`
- 管理员登录态访问首页 `/` 会自动跳转后台控制台

已验证账号示例：

```text
admin / 123456
user1 / 123456
user2 / 123456
user3 / 123456
user_test / 123456
```

密码方案仍为课程项目中的 MD5。旧明文密码兼容逻辑仍保留，旧明文登录成功后会自动升级为 MD5。

## OSS 上传

图片上传已接入阿里云 OSS，流程为：

```text
先保存到 static/uploads/<module>/，再上传 OSS，数据库保存 OSS URL。
```

当前覆盖：

- 作品封面和组图
- 论坛帖子配图
- 用户头像
- 公告封面
- 轮播图

`config.py` 从 `.env` 或环境变量读取 OSS 密钥，不要把 AccessKey 写入代码仓库。

PowerShell 示例：

```powershell
$env:OSS_ACCESS_KEY_ID="你的 AccessKey ID"
$env:OSS_ACCESS_KEY_SECRET="你的 AccessKey Secret"
$env:OSS_ENDPOINT="oss-cn-wuhan-lr.aliyuncs.com"
$env:OSS_BUCKET_NAME="photo-manage-oss"
$env:OSS_UPLOAD_PREFIX="photo-manage-platform"
$env:OSS_BUCKET_DOMAIN="photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com"
python app.py
```

如果修改了 `.env` 或环境变量，需要重启 Flask/PyCharm 运行进程后才会生效。`OSS_ENDPOINT`、`OSS_BUCKET_NAME`、`OSS_BUCKET_DOMAIN` 在 `config.py` 中有默认值，真正必须提供的是 `OSS_ACCESS_KEY_ID` 和 `OSS_ACCESS_KEY_SECRET`。

上传文件大小由 `MAX_IMAGE_SIZE` 控制，单位为字节；例如 20MB 可配置为 `20971520`。

## 轮播图

- 后台管理入口：`/admin/carousel/list`
- 新增入口：`/admin/carousel/add`
- 首页 `/` 已展示启用状态的轮播图
- 只展示 `status == 1` 的轮播图
- 当前 SQL 内置 3 条轮播测试图：`test`、`test2`、`test3`

## 首页精选作品

- 首页精选作品来自 `photo_work.is_featured = 1` 且审核通过、上架的作品。
- 精选状态由管理员在 `/admin/work/add` 和 `/admin/work/edit/<work_id>` 中维护。
- 摄影师前台发布或编辑自己的作品时不能设置首页精选。
- 首页作品、作品列表、作品详情、摄影师列表和摄影师主页都会过滤已禁用或已删除用户关联的摄影师。

## 首页公告

- 首页 `/` 会读取最新一条已发布公告，并以弹窗方式展示。
- 顶部导航的 `公告` 入口仍指向 `/announcement/list`，用于查看全部已发布公告。
- 弹窗中的 `不再弹出此公告` 只有被勾选时才会写入浏览器 `localStorage`。
- 如果没有勾选，下次进入首页仍会再次弹出同一条公告。
- 测试时可在浏览器控制台清理本地隐藏记录：

```javascript
Object.keys(localStorage).filter(k => k.startsWith('hiddenAnnouncement:')).forEach(k => localStorage.removeItem(k))
```

## 论坛发帖

- 普通用户登录后，导航栏昵称左侧有独立的 `发布帖子` 入口：`/forum/post_add`
- 也可以在某个板块帖子列表中进入 `/forum/post_add/<board_id>`，会默认选中当前板块
- 发帖表单通过下拉菜单选择板块，不再手动输入板块名
- 用户可编辑自己发布的帖子：`/forum/post_edit/<post_id>`
- 编辑帖子时可修改标题、内容、所属板块，可追加新图片，也可删除旧图片
- 帖子详情页和个人中心会给帖子作者显示编辑入口

## 摄影师前台作品管理

- 摄影师用户可在个人中心查看认证状态，并通过 `/user/edit_photographer` 完善真实姓名和所在城市
- 摄影师认证通过后，前台导航和个人中心会显示 `发布作品` 与 `我的作品` 入口
- 审核通过的摄影师进入个人中心时，页面默认直接展示 `我的作品`，下方再展示 `我的帖子`
- 发布作品入口：`/work/add`；我的作品入口：`/work/my`
- 摄影师可编辑自己的作品：`/work/edit/<work_id>`，支持替换封面、追加组图、删除旧组图
- 摄影师可通过 `/work/status/<work_id>` 下架或恢复自己的作品
- 摄影师前台发布的作品默认 `audit_status = 1`、`status = 1`，保存后直接在前台展示
- 摄影师只能管理自己名下的作品，不能选择或修改其他摄影师的作品

## 用户管理

- 后台用户管理入口：`/admin/user/list`
- 用户可按用户名、角色和状态筛选；默认不显示已删除用户
- 支持启用/禁用用户，已删除用户不能直接启用或禁用，需要先恢复
- 支持软删除用户：删除后 `user.status = -1`，可通过状态筛选查看并恢复
- 禁用或删除摄影师用户后，前台首页、摄影师列表、摄影师主页和公开作品展示会隐藏该摄影师相关内容

## 后台功能入口

- 控制台与图表：`/admin/dashboard/`
- 作品管理：`/admin/work/list`
- 作品评论管理：`/admin/work/comment_list`
- 摄影师审核：`/admin/photographer/list`
- 分类管理：`/admin/category/list`
- 用户管理：`/admin/user/list`
- 论坛帖子管理：`/admin/forum/post_list`
- 论坛板块管理：`/admin/forum/board_list`
- 论坛评论管理：`/admin/forum/comment_list`
- 公告管理：`/admin/announcement/list`，支持发布、编辑、上下架和删除
- 轮播图管理：`/admin/carousel/list`
- 系统日志：`/admin/system/logs`

## 演示与安全说明

- SQL 演示账号密码均为 `123456`，密码以 MD5 写入。
- 登录表单使用 POST 提交；直接 GET `/auth/login` 只渲染登录页，不提交账号密码。
- 项目已启用 Flask-WTF CSRF 防护，所有 POST 表单需要 `csrf_token`，Ajax 请求通过 `X-CSRFToken` 请求头提交。
- 前台和后台基础模板已加入通用 POST 表单重复提交防护；提交后按钮会禁用并显示 `处理中...`，避免重复点击造成重复上传或重复保存。
- 作品评论提交后默认通过，写入 `audit_status = 1`；后台作品评论管理只做启用/禁用，不做评论审核通过/拒绝操作。
- 如果运行时报 `No module named 'flask_wtf'`，请在项目虚拟环境执行 `python -m pip install -r requirements.txt`。
- 演示图片使用占位 URL；正式演示可在后台上传真实图片，数据库会保存 OSS URL。
- 不要提交 `environment.md`、`.env` 或任何含有 OSS AccessKey 的文件。
- 如密钥曾经暴露到不可信环境，应在阿里云控制台禁用或轮换。
- 后台图表默认从 CDN 加载 ECharts；如果演示环境不能联网，页面会显示表格降级数据。

## 常用验证

编码与模板检查：

```powershell
python -c "from pathlib import Path; files=list(Path('templates').rglob('*.html'))+[Path('README.md'),Path('HANDOFF.md'),Path('photography-platform-design-plan.md'),Path('photo_manage_platform.sql'),Path('.env.example')]; [p.read_text(encoding='utf-8') for p in files if p.exists()]; print('utf-8 ok', len(files))"
python -c "from pathlib import Path; from jinja2 import Environment, FileSystemLoader; env=Environment(loader=FileSystemLoader('templates')); [env.parse(p.read_text(encoding='utf-8')) for p in Path('templates').rglob('*.html')]; print('jinja syntax ok')"
python -c "from pathlib import Path; from app import app; [app.jinja_env.get_template(p.relative_to('templates').as_posix()) for p in Path('templates').rglob('*.html')]; print('flask jinja load/compile ok')"
```

如果终端输出出现类似 `鎽勫奖`、`歿{...}`、`?/a>` 的乱码，先按 UTF-8 读取文件或通过浏览器响应确认。当前已验证文件本身不是乱码损坏，不要因此直接改文件编码或全量替换模板文案。

```powershell
python -m compileall app.py views models utils
python -c "import app; print('import ok')"
python -c "from app import app; c=app.test_client(); paths=['/','/work/list','/photographer/list','/forum/board','/announcement/list','/auth/login']; print([(p,c.get(p).status_code) for p in paths])"
python -c "from app import app; c=app.test_client(); c.post('/auth/login', data={'username':'admin','password':'123456'}); paths=['/admin/dashboard/','/admin/work/comment_list','/admin/forum/board_list','/admin/system/logs']; print([(p,c.get(p).status_code) for p in paths])"
```
