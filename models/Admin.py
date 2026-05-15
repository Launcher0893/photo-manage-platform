"""管理员模型，对应数据库表 admin。

管理员和普通用户是两张表，但都接入 Flask-Login。
管理员 get_id() 返回 admin:<id>，普通用户返回 user:<id>。
"""

from datetime import datetime
from flask_login import UserMixin

from db import db


class Admin(db.Model, UserMixin):
    """后台管理员账号。"""
    __tablename__ = 'admin'
    
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_account = db.Column(db.String(50), unique=True, nullable=False)
    admin_password = db.Column(db.String(100), nullable=False)
    admin_name = db.Column(db.String(30), nullable=False)
    role_id = db.Column(
        db.Integer,
        db.ForeignKey('role.role_id', ondelete='RESTRICT'),
        nullable=True
    )
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 视图和模板通过 is_admin 判断当前登录者是不是管理员。
    is_admin = True

    @property
    def is_active(self):
        return self.status == 1
    
    def get_id(self):
        return f'admin:{self.admin_id}'

    @property
    def username(self):
        return self.admin_account

    @property
    def nickname(self):
        return self.admin_name

    @property
    def email(self):
        return ''

    @property
    def phone(self):
        return ''

    @property
    def avatar_url(self):
        return ''
    
    def __repr__(self):
        return f'<Admin {self.admin_name}>'
