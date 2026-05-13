# photo-manage-platform

摄影作品分享平台 Flask 课程项目。

## 运行说明

- 当前真实项目目录：`D:\Program Files\Code\PyCharm\photo-manage-platform`
- 默认数据库：本机 MySQL `photo_manage_platform`
- 默认连接串在 `config.py` 中，可通过环境变量 `DATABASE_URL` 覆盖
- 首次运行前需要先导入 `photo_manage_platform.sql`
- 本项目使用 Flask、SQLAlchemy、Flask-Login、MySQL、Bootstrap

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

`config.py` 中需要配置：

```python
OSS_ENABLED = True
OSS_ACCESS_KEY_ID = '...'
OSS_ACCESS_KEY_SECRET = '...'
OSS_ENDPOINT = 'oss-cn-wuhan-lr.aliyuncs.com'
OSS_BUCKET_NAME = 'photo-manage-oss'
OSS_UPLOAD_PREFIX = 'photo-manage-platform'
OSS_BUCKET_DOMAIN = 'photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com'
```

测试环境可以临时写入 AccessKey，但不要提交到公共仓库或公开截图。

## 轮播图

- 后台管理入口：`/admin/carousel/list`
- 新增入口：`/admin/carousel/add`
- 首页 `/` 已展示启用状态的轮播图
- 只展示 `status == 1` 的轮播图

## 常用验证

```powershell
python -m compileall app.py views models utils
python -c "import app; print('import ok')"
python -c "from app import app; c=app.test_client(); paths=['/','/work/list','/photographer/list','/forum/board','/announcement/list','/auth/login']; print([(p,c.get(p).status_code) for p in paths])"
```
