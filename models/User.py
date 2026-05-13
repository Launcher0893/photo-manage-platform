from datetime import datetime
from flask_login import UserMixin

from db import db


class User(db.Model, UserMixin):
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
    
    photographer = db.relationship(
        'Photographer',
        back_populates='user',
        uselist=False,
        passive_deletes='all',
    )
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
