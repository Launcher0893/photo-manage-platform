from db import db
from datetime import datetime

class PhotoWorkImage(db.Model):
    __tablename__ = 'photo_work_image'
    
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    work_id = db.Column(
        db.Integer,
        db.ForeignKey('photo_work.work_id', ondelete='CASCADE'),
        nullable=False
    )
    image_url = db.Column(db.String(255), nullable=False)
    oss_object_name = db.Column(db.String(255))
    sort = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<PhotoWorkImage {self.image_url}>'
