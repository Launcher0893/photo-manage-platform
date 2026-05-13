from db import db
from datetime import datetime

class Photographer(db.Model):
    __tablename__ = 'photographer'
    
    photographer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.user_id', ondelete='RESTRICT'),
        unique=True,
        nullable=False
    )
    real_name = db.Column(db.String(30))
    city = db.Column(db.String(50))
    cert_status = db.Column(db.SmallInteger, default=0)
    cert_remark = db.Column(db.String(255))
    audit_admin_id = db.Column(
        db.Integer,
        db.ForeignKey('admin.admin_id', ondelete='SET NULL'),
        nullable=True
    )
    audit_time = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    works = db.relationship('PhotoWork', backref='photographer', lazy=True, passive_deletes='all')
    
    STATUS_PENDING = 0
    STATUS_APPROVED = 1
    STATUS_REJECTED = 2
    
    def __repr__(self):
        return f'<Photographer {self.real_name}>'
