"""论坛帖子图片模型，对应数据库表 forum_post_image。

帖子可以上传多张图片，图片 URL 用于页面展示，oss_object_name 用于删除 OSS 文件。
"""

from db import db
from datetime import datetime

class ForumPostImage(db.Model):
    """论坛帖子图片表。"""
    __tablename__ = 'forum_post_image'
    
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('forum_post.post_id', ondelete='CASCADE'),
        nullable=False
    )
    image_url = db.Column(db.String(255), nullable=False)
    oss_object_name = db.Column(db.String(255))
    sort = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<ForumPostImage {self.image_url}>'
