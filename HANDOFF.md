# 摄影作品分享平台交接文档

## 新会话提示词

你现在接手一个 Flask 课程项目，项目是“摄影作品分享平台”。请先不要盲目改代码，先读取项目结构和关键文件，再根据用户当前要求继续实现。

当前有两个容易混淆的目录：

- `D:\Program Files\Code\PyCharm\photo_manage_platform`：早期规划文档目录，主要存放需求、设计计划、Git 协作文档等。
- `D:\Program Files\Code\PyCharm\photo-manage-platform`：当前真正的 Flask 项目目录，后续实现应优先在这个目录下进行。

项目技术栈：

- Python
- Flask
- HTML5 + CSS + JavaScript
- Bootstrap
- MySQL
- SQLAlchemy
- Flask-Login
- Git
- 后续可能接入阿里云 OSS 上传

重要文件：

- `photo-platform-requirements.md`：项目需求
- `photography-platform-design-plan.md`：详细设计计划
- `photo_manage_platform.sql`：数据库 SQL，当前应作为数据库结构源头
- `app.py`：Flask 入口，初始化 Flask、SQLAlchemy、Flask-Login 并注册蓝图
- `config.py`：数据库和 Flask 配置
- `db.py`：SQLAlchemy 实例
- `models/*.py`：模型
- `views/*.py`：蓝图路由
- `templates/**/*.html`：页面模板
- `utils/file_upload.py`：本地图片上传工具
- `utils/encryption.py`：MD5 密码和旧明文密码兼容迁移工具
- `utils/decorators.py`：普通用户/管理员权限装饰器

## 已确定的业务规则

- 不需要收藏功能，不存在 `work_favorite` 表，也不要重新引入 favorite/收藏相关功能。
- `photographer` 摄影师认证资料不包含“摄影师简介”和“从业年限”。
- `category` 分类表不包含“分类描述”。
- `photo_work` 摄影作品表不包含“收藏数”。
- 外键是否允许为空、删除级联策略应与 `photo_manage_platform.sql` 保持一致。
- 后台管理路由使用 `/admin/<module>/...`。
- 用户侧路由使用 `/work/...`、`/photographer/...`、`/forum/...`、`/announcement/...`。
- 作品互动 API 使用 `/api/work/<work_id>/like` 和 `/api/work/<work_id>/comment`。
- 当前密码方案仍是课程项目里的 MD5；不要在没有明确要求时切换到 Werkzeug/PBKDF2。

## 当前实现状态

- `app.py` 已经初始化 Flask、SQLAlchemy、Flask-Login，并注册多个蓝图。
- `/` 已经渲染真实数据库中的精选作品、热门作品、最新作品和摄影师。
- 登录注册已经接入真实数据库：
  - 普通用户登录：`/auth/login`
  - 管理员登录：`/auth/admin_login`
  - 注册：`/auth/register`
  - Flask-Login 的 `get_id()` 使用 `user:<id>` 和 `admin:<id>` 前缀。
- 密码问题已修复：
  - 新注册/改密写入 MD5。
  - 旧数据中如果密码是明文 `123456`，登录成功后会自动升级为 MD5。
  - 本机数据库里 `admin`、`user1`、`user2`、`user3`、`user_test` 的 `123456` 密码已经验证并升级为 MD5。
- 作品相关已接真实数据库：
  - 前台作品列表、详情、浏览量、点赞、评论。
  - 后台作品列表、新增、编辑、审核、下架。
  - 作品封面和组图保存到本地 `static/uploads/works/`。
- 摄影师相关已接真实数据库：
  - 前台摄影师列表/详情。
  - 后台摄影师审核，通过/拒绝时写入审核状态、备注、审核管理员和审核时间。
- 分类、用户、公告、轮播图、论坛、后台控制台均已从演示数据迁移到 SQLAlchemy 查询和写入。
- 本地图片上传策略：
  - 保存到 `static/uploads/<module>/`。
  - 数据库保存 `/static/uploads/<module>/<filename>`。
  - 当前未接 OSS，`utils/oss_utils.py` 仍是占位。
- `utils/demo_data.py` 仍在项目中，但当前主要业务路由已不再依赖它。

## 最近验证结果

已经通过以下检查：

```powershell
python -m compileall app.py views models utils
python -c "import app; print('import ok')"
```

前台核心页面检查：

```powershell
python -c "from app import app; c=app.test_client(); paths=['/','/work/list','/photographer/list','/forum/board','/announcement/list']; print([(p,c.get(p).status_code) for p in paths])"
```

结果均为 `200`。

后台未登录访问 `/admin/dashboard/` 返回 `302`，跳转到 `/auth/admin_login`，这是预期权限行为。

管理员会话注入后，以下后台页面曾验证为 `200`：

- `/admin/dashboard/`
- `/admin/work/list`
- `/admin/category/list`
- `/admin/user/list`
- `/admin/photographer/list`
- `/admin/announcement/list`
- `/admin/carousel/list`
- `/admin/forum/post_list`
- `/admin/forum/comment_list`
- `/admin/work/add`
- `/admin/category/add`
- `/admin/announcement/add`
- `/admin/carousel/add`

密码验证结果：

- `admin / 123456` 登录成功。
- `user1 / 123456`、`user2 / 123456`、`user3 / 123456` 登录成功。
- `user_test / 123456` 登录成功。
- 错误密码登录失败。

## Git 状态注意事项

当前仓库目录：

```powershell
cd "D:\Program Files\Code\PyCharm\photo-manage-platform"
```

继续工作前先运行：

```powershell
git status --short
```

注意：

- 当前工作区有大量未提交修改，这是前几轮实现产生的正常状态，不要用 `git reset --hard` 或 `git checkout --` 回退。
- `models/__init__.py` 是未跟踪文件，但当前 `app.py` 和多个路由依赖 `from models import ...`，不要删除。
- 修改前先读取相关文件，确认现状后再改。
- 如果只是在排查问题，优先只读检查，不要直接改代码或数据库。

## 已知问题和后续建议

1. 多个模板和早期文档曾出现中文乱码，部分文件已经恢复为可读中文，后续如果修 UI 文案，应逐个模板检查，不要盲目全量替换。
2. 当前上传是本地保存，后续如果接阿里云 OSS，应集中改 `utils/file_upload.py` 或新增上传适配层，不要把 OSS 逻辑散落到各蓝图。
3. 后台部分删除操作当前多为“状态切换/软删除”，应与课程需求和 SQL 表字段保持一致。
4. `photo_manage_platform.sql` 当前主要是表结构，未包含完整预置数据 INSERT；如果要交付可复现数据库，应补充初始化数据脚本，并确保密码写入 MD5。
5. 每次修改后至少运行导入检查和核心路由检查。

## 建议新会话第一步检查

```powershell
cd "D:\Program Files\Code\PyCharm\photo-manage-platform"
git status --short
Get-Content -Raw app.py
Get-Content -Raw views\auth.py
Get-Content -Raw utils\encryption.py
rg -n "demo_data|favorite|work_favorite|收藏|favorite" views models templates utils app.py
```

验证 Flask 导入：

```powershell
python -c "import app; print('import ok')"
```

验证核心页面：

```powershell
python -c "from app import app; c=app.test_client(); paths=['/','/work/list','/photographer/list','/forum/board','/announcement/list','/auth/login','/auth/admin_login']; print([(p,c.get(p).status_code) for p in paths])"
```

如果要验证后台页面，可先确认本机数据库中有管理员 `admin / 123456`，再通过页面登录后台，或用 test client 注入 `admin:1` 会话做只读检查。
