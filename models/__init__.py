"""模型统一导出文件。

其他文件可以写 `from models import User, PhotoWork`，
就是因为这里把各个模型类集中 import 进来了。
"""

from .Admin import Admin
from .Announcement import Announcement
from .Carousel import Carousel
from .Category import Category
from .ForumBoard import ForumBoard
from .ForumComment import ForumComment
from .ForumPost import ForumPost
from .ForumPostImage import ForumPostImage
from .ForumPostLike import ForumPostLike
from .PhotoWork import PhotoWork
from .PhotoWorkImage import PhotoWorkImage
from .Photographer import Photographer
from .Role import Role
from .SystemLog import SystemLog
from .User import User
from .WorkComment import WorkComment
from .WorkLike import WorkLike

__all__ = [
    'Admin',
    'Announcement',
    'Carousel',
    'Category',
    'ForumBoard',
    'ForumComment',
    'ForumPost',
    'ForumPostImage',
    'ForumPostLike',
    'PhotoWork',
    'PhotoWorkImage',
    'Photographer',
    'Role',
    'SystemLog',
    'User',
    'WorkComment',
    'WorkLike',
]
