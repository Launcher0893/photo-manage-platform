"""论坛帖子模型，对应数据库表 forum_post。

一条 ForumPost 表示用户发布的一篇帖子。
它属于一个论坛板块 forum_board，也属于一个发帖用户 user。
"""

from db import db
from datetime import datetime

class ForumPost(db.Model):
    """论坛帖子主表。"""
    __tablename__ = 'forum_post'
    
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    board_id = db.Column(
        db.Integer,
        db.ForeignKey('forum_board.board_id', ondelete='RESTRICT'),
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False
    )
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    view_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    is_top = db.Column(db.SmallInteger, default=0)
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关联发帖用户、帖子图片、评论和点赞记录。
    user = db.relationship('User', back_populates='forum_posts')
    images = db.relationship('ForumPostImage', backref='forum_post', lazy=True, passive_deletes='all')
    comments = db.relationship('ForumComment', backref='forum_post', lazy=True, passive_deletes='all')
    likes = db.relationship(
        'ForumPostLike',
        back_populates='forum_post',
        lazy=True,
        passive_deletes='all',
    )
    
    def __repr__(self):
        return f'<ForumPost {self.title}>'
