# photo-manage-platform

摄影作品分享平台 Flask 课程项目。

## 运行说明

- 当前真实项目目录：`D:\Program Files\Code\PyCharm\photo-manage-platform`
- 默认数据库：本机 MySQL `photo_manage_platform`
- 默认连接串在 `config.py` 中，可通过环境变量 `DATABASE_URL` 覆盖
- 首次运行前需要先导入 `photo_manage_platform.sql`
- 本项目使用 Flask、SQLAlchemy、Flask-Login、MySQL、Bootstrap
- `photo_manage_platform.sql` 已包含基础演示数据，导入后可直接使用下方账号登录

启动：

```powershell
cd "D:\Program Files\Code\PyCharm\photo-manage-platform"
python app.py
```

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

`config.py` 从环境变量读取 OSS 密钥，不要把 AccessKey 写入代码仓库。

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

如果修改了环境变量，需要重启 Flask/PyCharm 运行进程后才会生效。`OSS_ENDPOINT`、`OSS_BUCKET_NAME`、`OSS_BUCKET_DOMAIN` 在 `config.py` 中有默认值，真正必须提供的是 `OSS_ACCESS_KEY_ID` 和 `OSS_ACCESS_KEY_SECRET`。

## 轮播图

- 后台管理入口：`/admin/carousel/list`
- 新增入口：`/admin/carousel/add`
- 首页 `/` 已展示启用状态的轮播图
- 只展示 `status == 1` 的轮播图

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
- 公告管理：`/admin/announcement/list`
- 轮播图管理：`/admin/carousel/list`
- 系统日志：`/admin/system/logs`

## 演示与安全说明

- SQL 演示账号密码均为 `123456`，密码以 MD5 写入。
- 演示图片使用占位 URL；正式演示可在后台上传真实图片，数据库会保存 OSS URL。
- 不要提交 `environment.md`、`.env` 或任何含有 OSS AccessKey 的文件。
- 如密钥曾经暴露到不可信环境，应在阿里云控制台禁用或轮换。
- 后台图表默认从 CDN 加载 ECharts；如果演示环境不能联网，页面会显示表格降级数据。

## 常用验证

```powershell
python -m compileall app.py views models utils
python -c "import app; print('import ok')"
python -c "from app import app; c=app.test_client(); paths=['/','/work/list','/photographer/list','/forum/board','/announcement/list','/auth/login']; print([(p,c.get(p).status_code) for p in paths])"
python -c "from app import app; c=app.test_client(); c.post('/auth/login', data={'username':'admin','password':'123456'}); paths=['/admin/dashboard/','/admin/work/comment_list','/admin/forum/board_list','/admin/system/logs']; print([(p,c.get(p).status_code) for p in paths])"
```
