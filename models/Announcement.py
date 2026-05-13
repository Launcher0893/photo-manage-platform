from db import db
from datetime import datetime

class Announcement(db.Model):
    __tablename__ = 'announcement'
    
    announcement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    cover_url = db.Column(db.String(255))
    admin_id = db.Column(
        db.Integer,
        db.ForeignKey('admin.admin_id', ondelete='RESTRICT'),
        nullable=False
    )
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<Announcement {self.title}>'
