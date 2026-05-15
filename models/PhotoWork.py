"""作品模型，对应数据库表 photo_work。

一条 PhotoWork 表示一张摄影作品。
它关联摄影师 photographer、分类 category、组图 images、点赞 likes 和评论 comments。
"""

from db import db
from datetime import datetime

class PhotoWork(db.Model):
    """摄影作品主表。"""
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

    # relationship 是 ORM 关系，不是数据库字段；用于在 Python 中访问关联对象。
    photographer = db.relationship('Photographer', back_populates='works')
    category = db.relationship('Category', back_populates='works')
    images = db.relationship('PhotoWorkImage', backref='photo_work', lazy=True, passive_deletes='all')
    likes = db.relationship(
        'WorkLike',
        back_populates='photo_work',
        lazy=True,
        passive_deletes='all',
    )
    comments = db.relationship(
        'WorkComment',
        back_populates='photo_work',
        lazy=True,
        passive_deletes='all',
    )
    
    AUDIT_PENDING = 0
    AUDIT_APPROVED = 1
    AUDIT_REJECTED = 2
    
    def __repr__(self):
        return f'<PhotoWork {self.title}>'
    
    def update_hot_score(self):
        """更新热度分：浏览量 + 点赞数*3 + 评论数*2。"""
        self.hot_score = (
            (self.view_count or 0)
            + (self.like_count or 0) * 3
            + (self.comment_count or 0) * 2
        )
