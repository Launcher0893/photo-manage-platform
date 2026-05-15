"""论坛评论模型，对应数据库表 forum_comment。

一条记录表示某个用户对某篇帖子发表了一条评论。
"""

from db import db
from datetime import datetime

class ForumComment(db.Model):
    """论坛帖子评论表。"""
    __tablename__ = 'forum_comment'
    
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('forum_post.post_id', ondelete='CASCADE'),
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False
    )
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<ForumComment {self.comment_id}>'
