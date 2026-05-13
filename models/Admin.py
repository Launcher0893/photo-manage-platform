from db import db
from datetime import datetime

class Admin(db.Model):
    __tablename__ = 'admin'
    
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_account = db.Column(db.String(50), unique=True, nullable=False)
    admin_password = db.Column(db.String(100), nullable=False)
    admin_name = db.Column(db.String(30), nullable=False)
    role_id = db.Column(
        db.Integer,
        db.ForeignKey('role.role_id', ondelete='RESTRICT'),
        nullable=True
    )
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def is_active(self):
        return self.status == 1
    
    def get_id(self):
        return str(self.admin_id)
    
    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def __repr__(self):
        return f'<Admin {self.admin_name}>'
