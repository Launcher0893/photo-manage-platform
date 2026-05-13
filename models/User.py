from db import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(30))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    avatar_url = db.Column(db.String(255))
    user_role = db.Column(db.SmallInteger, default=1)
    status = db.Column(db.SmallInteger, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    photographer = db.relationship('Photographer', backref='user', uselist=False, passive_deletes='all')
    work_likes = db.relationship('WorkLike', backref='user', lazy=True, passive_deletes='all')
    work_comments = db.relationship('WorkComment', backref='user', lazy=True, passive_deletes='all')
    forum_posts = db.relationship('ForumPost', backref='user', lazy=True, passive_deletes='all')
    forum_comments = db.relationship('ForumComment', backref='user', lazy=True, passive_deletes='all')
    
    ROLE_NORMAL = 1
    ROLE_PHOTOGRAPHER = 2
    
    def is_active(self):
        return self.status == 1
    
    def get_id(self):
        return str(self.user_id)
    
    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def __repr__(self):
        return f'<User {self.username}>'
