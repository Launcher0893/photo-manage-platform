from db import db
from datetime import datetime

class SystemLog(db.Model):
    __tablename__ = 'system_log'
    
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(
        db.Integer,
        db.ForeignKey('admin.admin_id', ondelete='RESTRICT'),
        nullable=False
    )
    operate_type = db.Column(db.String(30), nullable=False)
    operate_content = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(50))
    operate_time = db.Column(db.DateTime, default=datetime.now)
    admin = db.relationship('Admin', backref='system_logs')
    
    def __repr__(self):
        return f'<SystemLog {self.operate_type}>'
