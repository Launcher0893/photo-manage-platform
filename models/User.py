"""用户模型，对应数据库表 user。

普通用户和摄影师账号都存在这张表里。
user_role 区分普通用户和摄影师，status 控制正常/禁用/软删除。
"""

from datetime import datetime
from flask_login import UserMixin

from db import db


class User(db.Model, UserMixin):
    """前台用户账号。

    UserMixin 让它可以被 Flask-Login 登录系统使用。
    get_id() 返回 user:<id>，用于和管理员 admin:<id> 区分。
    """
    __tablename__ = 'user'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(30))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    avatar_url = db.Column(db.String(255))
    user_role = db.Column(db.SmallInteger, default=1)
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 一个用户最多有一条摄影师认证资料，对应 photographer 表。
    photographer = db.relationship(
        'Photographer',
        back_populates='user',
        uselist=False,
        passive_deletes='all',
    )
    # 用户点赞、评论、发帖等关系，方便通过 current_user 反查相关数据。
    work_likes = db.relationship(
        'WorkLike',
        back_populates='user',
        lazy=True,
        passive_deletes='all',
    )
    work_comments = db.relationship(
        'WorkComment',
        back_populates='user',
        lazy=True,
        passive_deletes='all',
    )
    forum_posts = db.relationship(
        'ForumPost',
        back_populates='user',
        lazy=True,
        passive_deletes='all',
    )
    forum_comments = db.relationship('ForumComment', backref='user', lazy=True, passive_deletes='all')
    forum_post_likes = db.relationship(
        'ForumPostLike',
        back_populates='user',
        lazy=True,
        passive_deletes='all',
    )
    
    ROLE_NORMAL = 1
    ROLE_PHOTOGRAPHER = 2
    
    is_admin = False

    @property
    def is_active(self):
        return self.status == 1
    
    def get_id(self):
        return f'user:{self.user_id}'
    
    def __repr__(self):
        return f'<User {self.username}>'
