from db import db
from datetime import datetime

class PhotoWork(db.Model):
    __tablename__ = 'photo_work'
    
    work_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    photographer_id = db.Column(
        db.Integer,
        db.ForeignKey('photographer.photographer_id', ondelete='RESTRICT'),
        nullable=False
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('category.category_id', ondelete='RESTRICT'),
        nullable=False
    )
    cover_url = db.Column(db.String(255))
    city = db.Column(db.String(50))
    description = db.Column(db.Text)
    view_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    hot_score = db.Column(db.Integer, default=0)
    audit_status = db.Column(db.SmallInteger, default=0)
    is_featured = db.Column(db.SmallInteger, default=0)
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    images = db.relationship('PhotoWorkImage', backref='photo_work', lazy=True, passive_deletes='all')
    likes = db.relationship('WorkLike', backref='photo_work', lazy=True, passive_deletes='all')
    comments = db.relationship('WorkComment', backref='photo_work', lazy=True, passive_deletes='all')
    
    AUDIT_PENDING = 0
    AUDIT_APPROVED = 1
    AUDIT_REJECTED = 2
    
    def __repr__(self):
        return f'<PhotoWork {self.title}>'
    
    def update_hot_score(self):
        self.hot_score = self.view_count + self.like_count * 3 + self.comment_count * 2
