from datetime import datetime

from db import db


class ForumPostLike(db.Model):
    __tablename__ = 'forum_post_like'

    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('forum_post.post_id', ondelete='CASCADE'),
        nullable=False,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.user_id', ondelete='CASCADE'),
        nullable=False,
    )
    create_time = db.Column(db.DateTime, default=datetime.now)

    forum_post = db.relationship('ForumPost', back_populates='likes')
    user = db.relationship('User', back_populates='forum_post_likes')

    __table_args__ = (
        db.UniqueConstraint('post_id', 'user_id', name='uk_forum_post_user'),
    )

    def __repr__(self):
        return f'<ForumPostLike {self.post_id}-{self.user_id}>'
