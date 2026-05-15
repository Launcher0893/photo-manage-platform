"""数据库对象文件。

这里创建一个全局 SQLAlchemy 对象 db。
app.py 里通过 db.init_app(app) 把它绑定到 Flask 应用。
models/*.py 中的 db.Model、db.Column、db.relationship 都来自这里。
"""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
