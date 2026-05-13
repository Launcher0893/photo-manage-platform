from db import db
from datetime import datetime

class WorkLike(db.Model):
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
    
    __table_args__ = (
        db.UniqueConstraint('work_id', 'user_id', name='uk_work_user'),
    )
    
    def __repr__(self):
        return f'<WorkLike {self.work_id}-{self.user_id}>'
