from db import db
from datetime import datetime

class ForumComment(db.Model):
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
