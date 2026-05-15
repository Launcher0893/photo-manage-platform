# 摄影作品分享平台答辩测试流程

本文档用于答辩前按固定顺序验证项目。原则是先验证项目能稳定启动和访问，再演示核心功能。严谨性优先，功能演示可按时间裁剪。

## 1. 测试环境

项目路径：

```text
D:\Program Files\Code\PyCharm\photo-manage-platform
```

技术栈：

```text
Flask
SQLAlchemy
Flask-Login
Flask-WTF CSRF
MySQL
Bootstrap
阿里云 OSS
```

启动前确认：

```text
1. MySQL 已启动
2. 已导入 photo_manage_platform.sql
3. .env 或 config.py 中 DATABASE_URL 可连接当前 MySQL
4. requirements.txt 依赖已安装
5. 如果不演示 OSS 上传，可设置 OSS_ENABLED=false
```

安装依赖：

```powershell
cd "D:\Program Files\Code\PyCharm\photo-manage-platform"
python -m pip install -r requirements.txt
```

启动项目：

```powershell
python app.py
```

浏览器访问：

```text
http://127.0.0.1:5000/
```

## 2. 本轮自动验证结果

本轮已在当前项目目录执行过以下验证。

Python 语法编译：

```powershell
python -m compileall app.py views models utils
```

结果：

```text
通过
```

Jinja 模板语法：

```powershell
python -c "from pathlib import Path; from jinja2 import Environment, FileSystemLoader; env=Environment(loader=FileSystemLoader('templates')); files=list(Path('templates').rglob('*.html')); [env.parse(p.read_text(encoding='utf-8')) for p in files]; print('jinja_parse_ok', len(files))"
```

结果：

```text
jinja_parse_ok 42
```

Flask 模板加载和路由注册：

```powershell
python -c "from pathlib import Path; from app import app; files=list(Path('templates').rglob('*.html')); [app.jinja_env.get_template(p.relative_to('templates').as_posix()) for p in files]; print('flask_template_load_ok', len(files)); print('routes', len(list(app.url_map.iter_rules())))"
```

结果：

```text
flask_template_load_ok 42
routes 80
```

公开页面访问结果：

```text
/                    200
/work/list           200
/photographer/list   200
/forum/board         200
/announcement/list   200
/auth/login          200
```

管理员登录和后台页面结果：

```text
POST /auth/login admin/123456     302 -> /admin/dashboard/index
/admin/dashboard/                 200
/admin/work/list                  200
/admin/photographer/list          200
/admin/category/list              200
/admin/user/list                  200
/admin/forum/post_list            200
/admin/announcement/list          200
/admin/carousel/list              200
/admin/system/logs                200
```

前台用户权限结果：

```text
Gemini / 123456
/user/profile      200
/forum/my          200
/forum/post_add    200
/work/add          302 -> /user/profile
```

摄影师权限结果：

```text
Launcher0893 / 123456
/user/profile      200
/forum/my          200
/forum/post_add    200
/work/add          200
```

说明：

```text
Gemini 是普通用户，不能发布作品，跳回个人中心符合预期。
Launcher0893 是审核通过摄影师，可以进入作品发布页符合预期。
```

## 3. 答辩演示账号

优先使用：

```text
管理员：admin / 123456
普通用户：Gemini / 123456
摄影师：Launcher0893 / 123456
```

如果本地数据库重新导入或数据不同，先在后台用户管理中确认用户 `status=1`。

## 4. 答辩前快速自检流程

建议答辩当天先执行这一组命令。

```powershell
cd "D:\Program Files\Code\PyCharm\photo-manage-platform"
python -m compileall app.py views models utils
python -c "from pathlib import Path; from jinja2 import Environment, FileSystemLoader; env=Environment(loader=FileSystemLoader('templates')); files=list(Path('templates').rglob('*.html')); [env.parse(p.read_text(encoding='utf-8')) for p in files]; print('jinja_parse_ok', len(files))"
python -c "from pathlib import Path; from app import app; files=list(Path('templates').rglob('*.html')); [app.jinja_env.get_template(p.relative_to('templates').as_posix()) for p in files]; print('flask_template_load_ok', len(files)); print('routes', len(list(app.url_map.iter_rules())))"
python app.py
```

预期：

```text
Python 编译无报错
jinja_parse_ok 42
flask_template_load_ok 42
routes 80
Flask 启动成功
```

## 5. 浏览器完整演示流程

### 5.1 首页展示

访问：

```text
http://127.0.0.1:5000/
```

检查点：

```text
顶部导航栏正常
首页 Hero 区域正常
轮播图正常显示
精选作品正常显示
热门作品正常显示
最新作品正常显示
推荐摄影师正常显示
最新公告弹窗正常显示
```

如果公告不弹出：

```text
可能是浏览器 localStorage 已记录“不再弹出此公告”
```

浏览器控制台执行：

```javascript
Object.keys(localStorage).filter(k => k.startsWith('hiddenAnnouncement:')).forEach(k => localStorage.removeItem(k))
```

刷新首页后再测。

### 5.2 前台作品浏览

访问：

```text
/work/list
```

检查点：

```text
作品列表正常
分类筛选正常
关键词搜索正常
城市筛选正常
热门/最新排序正常
分页正常
```

点击任意作品进入详情页：

```text
/work/detail/<work_id>
```

检查点：

```text
作品封面和组图正常
摄影师信息正常
分类、城市、描述正常
浏览量会增加
评论区正常显示
未登录时点赞/评论应提示登录
```

### 5.3 摄影师浏览

访问：

```text
/photographer/list
```

检查点：

```text
只展示审核通过且账号正常的摄影师
城市筛选正常
昵称搜索正常
点击摄影师主页正常
摄影师主页只展示公开上架作品
```

### 5.4 公告浏览

访问：

```text
/announcement/list
```

检查点：

```text
公告列表正常
公告详情正常
只展示已发布公告
首页公告弹窗链接可进入详情
```

### 5.5 论坛前台

访问：

```text
/forum/board
```

检查点：

```text
板块列表正常
每个板块帖子数正常
进入帖子列表正常
帖子搜索和排序正常
进入帖子详情正常
```

普通用户登录：

```text
/auth/login
Gemini / 123456
```

检查点：

```text
登录后导航栏显示发布帖子、我的帖子、用户中心、退出
/forum/post_add 可以发布帖子
/forum/my 可以查看我的帖子
自己的帖子可以编辑
帖子详情可以评论和点赞
```

### 5.6 摄影师作品管理

退出普通用户，登录摄影师：

```text
Launcher0893 / 123456
```

检查点：

```text
导航栏显示发布作品、我的作品
/work/add 可以进入发布作品页
/work/my 可以查看自己的作品
只能编辑自己的作品
可以下架/恢复自己的作品
发布作品默认 audit_status=1 且 status=1
```

如需避免 OSS 环境风险，答辩时可只演示进入页面和已有作品管理，不强依赖现场上传。

### 5.7 管理员后台

退出前台用户，登录管理员：

```text
admin / 123456
```

登录后应跳转：

```text
/admin/dashboard/
```

检查点：

```text
后台左侧菜单正常
控制台统计卡片正常
热门作品、最新用户、最新作品、热门帖子正常
图表区域正常
```

逐个进入后台菜单：

```text
/admin/work/list
/admin/photographer/list
/admin/category/list
/admin/user/list
/admin/forum/post_list
/admin/announcement/list
/admin/carousel/list
/admin/system/logs
```

检查点：

```text
所有页面能打开
筛选表单正常
分页正常
状态标签正常
操作按钮正常显示
```

重点演示建议：

```text
用户管理：启用/禁用、软删除/恢复
摄影师审核：查看审核状态，说明通过后才能发作品
作品管理：上架/下架、精选状态
分类管理：新增/编辑/启停分类
论坛管理：帖子置顶、隐藏/恢复帖子和评论
公告管理：发布/下架公告，首页弹窗读取最新发布公告
轮播图管理：启用/停用轮播图，首页只显示启用项
系统日志：后台关键操作会写入日志
```

## 6. 答辩讲解顺序

推荐按这个顺序讲，逻辑最顺：

```text
1. 项目目标：摄影作品分享平台，三类角色：普通用户、摄影师、管理员
2. 技术栈：Flask + SQLAlchemy + MySQL + Flask-Login + Flask-WTF + Bootstrap + OSS
3. 项目结构：app.py、views、models、templates、utils、SQL
4. 首页：轮播图、精选/热门/最新作品、摄影师推荐、公告弹窗
5. 登录权限：统一登录，普通用户和管理员自动识别
6. 前台作品：列表、详情、点赞、评论
7. 摄影师闭环：认证通过后发布和管理作品
8. 论坛：板块、帖子、发帖、编辑、评论、点赞
9. 后台：控制台和各管理模块
10. 安全与稳定：CSRF、防重复提交、软删除、OSS 密钥环境变量
```

## 7. 常见异常和现场处理

页面 404：

```text
URL 写错或路由不存在。
按 URL 去 views/*.py 查 @route 和蓝图 url_prefix。
```

页面 403：

```text
权限不够。
检查当前是否登录了正确角色，后台需要 admin，前台发帖/作品需要前台用户。
```

页面 500：

```text
看终端 traceback 最后一段。
常见原因是数据库连接失败、模板变量为空、OSS 配置缺失。
```

登录失败：

```text
确认账号存在且 status=1。
确认密码为 123456。
确认数据库使用的是当前 photo_manage_platform.sql。
```

上传失败：

```text
检查图片格式是否 jpg/jpeg/png/gif/webp。
检查大小是否超过 MAX_IMAGE_SIZE。
如果 OSS 配置不稳定，设置 OSS_ENABLED=false 后只演示本地上传。
```

中文显示乱码：

```text
优先确认浏览器页面是否正常。
PowerShell 输出乱码通常是终端编码问题，不代表文件损坏。
不要盲目批量修改文件编码。
```

## 8. 最小保底演示流程

如果答辩时间很短，按这个保底流程演示：

```text
1. 打开首页，展示轮播、作品、摄影师、公告
2. 打开作品列表和作品详情
3. 登录普通用户，展示发帖和个人中心
4. 登录摄影师，展示发布作品和我的作品
5. 登录管理员，展示后台控制台
6. 后台进入用户管理、作品管理、公告管理、系统日志
7. 说明 CSRF、防重复提交、软删除、OSS 环境变量
```

这个流程覆盖了项目主线，且不强依赖现场新增上传数据。
