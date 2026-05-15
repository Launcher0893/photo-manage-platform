"""论坛板块模型，对应数据库表 forum_board。

例如“作品交流”“技巧分享”等板块。
一个板块下可以有多篇帖子。
"""

from db import db
from datetime import datetime

class ForumBoard(db.Model):
    """论坛板块表。"""
    __tablename__ = 'forum_board'
    
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    board_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    sort = db.Column(db.Integer, default=0)
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    # posts 表示这个板块下的帖子列表。
    posts = db.relationship('ForumPost', backref='forum_board', lazy=True, passive_deletes='all')
    
    def __repr__(self):
        return f'<ForumBoard {self.board_name}>'
