"""摄影师认证资料模型，对应数据库表 photographer。

user 表保存账号；photographer 表保存摄影师真实姓名、城市、认证状态等资料。
一个 user 最多对应一条 photographer 记录。
"""

from db import db
from datetime import datetime

class Photographer(db.Model):
    """摄影师资料表。"""
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
    
    # user 是摄影师对应的账号；works 是该摄影师发布的作品列表。
    user = db.relationship('User', back_populates='photographer')
    works = db.relationship(
        'PhotoWork',
        back_populates='photographer',
        lazy=True,
        passive_deletes='all',
    )
    
    STATUS_PENDING = 0
    STATUS_APPROVED = 1
    STATUS_REJECTED = 2
    
    def __repr__(self):
        return f'<Photographer {self.real_name}>'
