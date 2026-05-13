from db import db
from datetime import datetime

class ForumBoard(db.Model):
    __tablename__ = 'forum_board'
    
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    board_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    sort = db.Column(db.Integer, default=0)
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    posts = db.relationship('ForumPost', backref='forum_board', lazy=True, passive_deletes='all')
    
    def __repr__(self):
        return f'<ForumBoard {self.board_name}>'
