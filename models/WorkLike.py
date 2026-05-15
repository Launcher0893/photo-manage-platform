"""作品点赞模型，对应数据库表 work_like。

一条记录表示某个用户点赞了某个作品。
UniqueConstraint 保证同一个用户不能重复点赞同一个作品。
"""

from db import db
from datetime import datetime

class WorkLike(db.Model):
    """作品点赞关系表。"""
    __tablename__ = 'work_like'
    
    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    work_id = db.Column(
        db.Integer,
        db.ForeignKey('photo_work.work_id', ondelete='CASCADE'),
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False
    )
    create_time = db.Column(db.DateTime, default=datetime.now)

    photo_work = db.relationship('PhotoWork', back_populates='likes')
    user = db.relationship('User', back_populates='work_likes')

    __table_args__ = (
        db.UniqueConstraint('work_id', 'user_id', name='uk_work_user'),
    )
    
    def __repr__(self):
        return f'<WorkLike {self.work_id}-{self.user_id}>'
