"""作品分类模型，对应数据库表 category。

作品发布/编辑时选择分类，作品列表也可以按分类筛选。
"""

from db import db
from datetime import datetime

class Category(db.Model):
    """作品分类表。"""
    __tablename__ = 'category'
    
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(50), unique=True, nullable=False)
    sort = db.Column(db.Integer, default=0)
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 一个分类下可以有多条作品。
    works = db.relationship(
        'PhotoWork',
        back_populates='category',
        lazy=True,
        passive_deletes='all',
    )
    
    def __repr__(self):
        return f'<Category {self.category_name}>'
