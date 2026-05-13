from db import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'category'
    
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(50), unique=True, nullable=False)
    sort = db.Column(db.Integer, default=0)
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    works = db.relationship('PhotoWork', backref='category', lazy=True, passive_deletes='all')
    
    def __repr__(self):
        return f'<Category {self.category_name}>'
