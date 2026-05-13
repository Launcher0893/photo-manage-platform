from db import db
from datetime import datetime

class Carousel(db.Model):
    __tablename__ = 'carousel'
    
    carousel_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    image_url = db.Column(db.String(255), nullable=False)
    link_type = db.Column(db.String(30))
    link_id = db.Column(db.Integer)
    link_url = db.Column(db.String(255))
    sort = db.Column(db.Integer, default=0)
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<Carousel {self.title}>'
