from db import db
from datetime import datetime

class Role(db.Model):
    __tablename__ = 'role'
    
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(30), nullable=False)
    permissions = db.Column(db.String(255))
    remark = db.Column(db.String(100))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    admins = db.relationship('Admin', backref='role', lazy=True, passive_deletes='all')
    
    def __repr__(self):
        return f'<Role {self.role_name}>'
