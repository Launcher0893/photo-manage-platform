# 摄影作品分享平台交接文档

## 新会话提示词

你现在接手一个 Flask 课程项目，项目是“摄影作品分享平台”。请先不要盲目改代码，先读取项目结构和关键文件，再根据用户当前要求继续实现。

当前有两个容易混淆的目录：

- `D:\Program Files\Code\PyCharm\photo_manage_platform`：早期规划文档目录，主要存放需求、设计计划、Git 协作文档和本交接文档。
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
- `app.py`：Flask 入口
- `config.py`：配置
- `db.py`：SQLAlchemy 实例
- `models/*.py`：模型
- `views/*.py`：蓝图路由
- `templates/**/*.html`：页面模板
- `utils/demo_data.py`：当前演示数据

## 已确定的业务规则

- 不需要收藏功能，所有“收藏 / favorite”相关内容都应删除或避免重新引入。
- `photographer` 摄影师认证资料不包含“摄影师简介”和“从业年限”。
- `category` 分类表不包含“分类描述”。
- `photo_work` 摄影作品表不包含“收藏数”。
- 不存在 `work_favorite` 作品收藏表。
- 外键是否允许为空、删除级联策略应与 `photo_manage_platform.sql` 保持一致。
- 后台管理路由使用 `/admin/<module>/...`。
- 用户侧路由使用 `/work/...`、`/photographer/...`、`/forum/...`、`/announcement/...`。
- 作品交互 API 使用 `/api/work/<work_id>/like` 和 `/api/work/<work_id>/comment`。

## 当前实现状态

- `app.py` 已经不是 Hello World，已经初始化 Flask、SQLAlchemy、Flask-Login，并注册多个蓝图。
- `/` 已经渲染 `index.html`，目标是显示“摄影作品分享平台”主页。
- `config.py` 当前为了便于启动，使用 `DATABASE_URL` 环境变量；没有配置时回退到本地 SQLite。
- 当前 `views` 多数还是演示路由，依赖 `utils/demo_data.py`，还没有全面接入真实数据库。
- 当前认证是演示版：
  - 登录表单基本是模拟登录。
  - 管理员登录也是模拟登录。
  - 还没有真实密码校验。
- 当前 API 是演示版：
  - 点赞、评论接口返回成功 JSON，但没有真实数据库写入。
- `templates` 已经做过一轮修复：
  - `base.html` 与 `admin_base.html` 已区分前台和后台。
  - 多个后台链接已统一为 `/admin/...`。
  - 多个上传表单字段已添加，例如作品封面、作品图片、公告封面、帖子图片、用户头像。

上一轮检查中，这些状态曾经通过：

- `import app` 成功。
- `GET /` 返回 `200`，页面包含“摄影作品分享平台”。
- `/work/list`、`/photographer/list`、`/forum/board`、`/announcement/list`、`/admin/dashboard/` 返回过 `200`。

## Git 状态注意事项

`D:\Program Files\Code\PyCharm\photo-manage-platfrom` 是当前真正的 Git 仓库。上一轮只读检查时发现有大量已修改文件和未跟踪文件，还没有提交。

继续工作前应先运行：

```powershell
cd "D:\Program Files\Code\PyCharm\photo-manage-platfrom"
git status --short
```

注意事项：

- 不要使用 `git reset --hard`、`git checkout --` 等破坏性命令。
- 不要覆盖用户已经写入的代码。
- 修改前先读取相关文件，确认现状。
- 如果只是检查问题，优先只读检查，不要直接改代码。

## 建议新会话第一步检查

```powershell
cd "D:\Program Files\Code\PyCharm\photo-manage-platfrom"
git status --short
Get-Content -Raw app.py
Get-ChildItem -Recurse -File views,templates,models,utils | Select-Object FullName
```

验证 Flask 导入：

```powershell
python -c "import app; print('import ok')"
```

验证核心页面：

```powershell
python -c "from app import app; c=app.test_client(); paths=['/','/work/list','/photographer/list','/forum/board','/announcement/list','/admin/dashboard/']; print([(p,c.get(p).status_code) for p in paths])"
```

## 下一步优先级建议

1. 先确认用户当前具体要求，是继续修页面、接真实数据库、修启动问题，还是实现某个功能模块。
2. 如果是“接数据库”，优先以 `photo_manage_platform.sql` 为准检查 `models/*.py`，再把 `views` 从 `demo_data` 改成 SQLAlchemy 查询。
3. 如果是“继续完善项目”，建议顺序为：真实用户 / 管理员登录、摄影作品列表和详情、作品上传、摄影师认证、公告管理、论坛帖子与评论、上传工具与 OSS。
4. 每次修改后运行导入检查和关键路由检查。
5. 回答用户时用中文，说明具体改了什么、检查结果是什么、还有什么没完成。

