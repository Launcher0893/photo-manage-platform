from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class DemoUser:
    user_id: int
    username: str
    nickname: str
    email: str = ''
    phone: str = ''
    avatar_url: str = ''
    user_role: int = 1
    status: int = 1
    is_admin: bool = False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.status == 1

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        prefix = 'admin' if self.is_admin else 'user'
        return f'{prefix}:{self.user_id}'


@dataclass
class DemoCategory:
    category_id: int
    category_name: str
    sort: int = 0
    status: int = 1


@dataclass
class DemoPhotographer:
    photographer_id: int
    user: DemoUser
    real_name: str = ''
    city: str = ''
    cert_status: int = 1
    cert_remark: str = ''
    create_time: datetime = field(default_factory=datetime.now)
    works: list = field(default_factory=list)


@dataclass
class DemoWork:
    work_id: int
    title: str
    photographer: DemoPhotographer | None
    category: DemoCategory | None
    cover_url: str = ''
    city: str = ''
    description: str = ''
    view_count: int = 0
    like_count: int = 0
    comment_count: int = 0
    hot_score: int = 0
    audit_status: int = 1
    is_featured: int = 0
    status: int = 1
    create_time: datetime = field(default_factory=datetime.now)


@dataclass
class DemoComment:
    comment_id: int
    user: DemoUser
    content: str
    create_time: datetime = field(default_factory=datetime.now)
    status: int = 1


@dataclass
class DemoBoard:
    board_id: int
    board_name: str
    description: str = ''
    posts: list = field(default_factory=list)


@dataclass
class DemoPost:
    post_id: int
    forum_board: DemoBoard
    user: DemoUser
    title: str
    content: str
    view_count: int = 0
    like_count: int = 0
    comment_count: int = 0
    is_top: int = 0
    status: int = 1
    create_time: datetime = field(default_factory=datetime.now)


@dataclass
class DemoAnnouncement:
    announcement_id: int
    title: str
    content: str
    cover_url: str = ''
    status: int = 1
    create_time: datetime = field(default_factory=datetime.now)


@dataclass
class Pagination:
    items: list
    page: int = 1

    @property
    def has_prev(self):
        return False

    @property
    def has_next(self):
        return False

    @property
    def prev_num(self):
        return 1

    @property
    def next_num(self):
        return 1

    def iter_pages(self):
        return [1]


user_normal = DemoUser(1, 'alice', 'Alice', email='alice@example.com', phone='13800000000')
user_photographer = DemoUser(2, 'bruce', 'Bruce', email='bruce@example.com', phone='13900000000', user_role=2)
admin_user = DemoUser(1, 'admin', '系统管理员', is_admin=True)

category_portrait = DemoCategory(1, '人像', 1)
category_street = DemoCategory(2, '街拍', 2)
categories = [category_portrait, category_street]

photographer_1 = DemoPhotographer(
    1,
    user_photographer,
    real_name='Bruce Lee',
    city='香港',
    cert_status=1,
    create_time=datetime.now() - timedelta(days=20)
)
photographers = [photographer_1]

work_1 = DemoWork(
    1,
    '夜色人像',
    photographer_1,
    category_portrait,
    city='上海',
    description='夜景环境下的人像摄影示例。',
    view_count=128,
    like_count=24,
    comment_count=3,
    hot_score=206,
    is_featured=1,
    create_time=datetime.now() - timedelta(days=2)
)
work_2 = DemoWork(
    2,
    '街头光影',
    photographer_1,
    category_street,
    city='广州',
    description='街头抓拍与光影层次示例。',
    view_count=96,
    like_count=18,
    comment_count=2,
    hot_score=154,
    create_time=datetime.now() - timedelta(days=1)
)
works = [work_1, work_2]
photographer_1.works = works

comments = [
    DemoComment(1, user_normal, '构图不错，光线也很干净。', datetime.now() - timedelta(hours=3)),
    DemoComment(2, user_photographer, '谢谢，后续还会继续更新。', datetime.now() - timedelta(hours=1))
]

board_1 = DemoBoard(1, '作品交流', '发布作品与交流拍摄经验')
board_2 = DemoBoard(2, '技巧分享', '讨论器材、后期和拍摄技巧')
boards = [board_1, board_2]

post_1 = DemoPost(1, board_1, user_normal, '第一次夜景拍摄心得', '分享一次夜景拍摄的参数设置。', 56, 8, 2, 1)
post_2 = DemoPost(2, board_2, user_photographer, '人像布光笔记', '简单整理常见的人像布光方式。', 42, 5, 1, 0)
posts = [post_1, post_2]
board_1.posts = [post_1]
board_2.posts = [post_2]

announcements = [
    DemoAnnouncement(1, '平台试运行公告', '摄影作品分享平台当前已完成基础页面接入。', create_time=datetime.now() - timedelta(days=1)),
    DemoAnnouncement(2, '作品征集说明', '欢迎上传街拍、人像、风光等类型作品。', create_time=datetime.now())
]


def get_home_context():
    return {
        'featured_works': [work_1],
        'hot_works': sorted(works, key=lambda item: item.hot_score, reverse=True),
        'recent_works': sorted(works, key=lambda item: item.create_time, reverse=True),
        'photographers': photographers,
    }


def get_user(user_id: int):
    users = {
        1: user_normal,
        2: user_photographer,
    }
    return users.get(user_id)


def get_admin():
    return admin_user


def get_work(work_id: int):
    for work in works:
        if work.work_id == work_id:
            return work
    return None


def get_photographer(photographer_id: int):
    for photographer in photographers:
        if photographer.photographer_id == photographer_id:
            return photographer
    return None


def get_board(board_id: int):
    for board in boards:
        if board.board_id == board_id:
            return board
    return None


def get_post(post_id: int):
    for post in posts:
        if post.post_id == post_id:
            return post
    return None


def get_announcement(announcement_id: int):
    for announcement in announcements:
        if announcement.announcement_id == announcement_id:
            return announcement
    return None
