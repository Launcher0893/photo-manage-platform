"""作品评论模型，对应数据库表 work_comment。

一条记录表示某个用户对某个作品发表了一条评论。
audit_status 是审核状态，status 是显示/隐藏状态。
"""

from db import db
from datetime import datetime

class WorkComment(db.Model):
    """作品评论表。"""
    __tablename__ = 'work_comment'
    
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    content = db.Column(db.Text, nullable=False)
    audit_status = db.Column(db.SmallInteger, default=1)
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    photo_work = db.relationship('PhotoWork', back_populates='comments')
    user = db.relationship('User', back_populates='work_comments')
    
    def __repr__(self):
        return f'<WorkComment {self.comment_id}>'
