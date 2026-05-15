"""项目配置文件。

这里集中配置 Flask 密钥、数据库连接、上传大小、OSS 参数。
优先读取系统环境变量或 .env 文件；如果没有配置，就使用默认值。
"""

import os

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if load_dotenv is not None:
    # 如果安装了 python-dotenv，就自动读取项目根目录下的 .env 本地配置文件。
    load_dotenv(os.path.join(BASE_DIR, '.env'))

DEFAULT_DATABASE_URL = (
    'mysql+pymysql://root:Sean20041218@127.0.0.1:3306/'
    'photo_manage_platform?charset=utf8mb4'
)


class Config:
    """Flask 应用配置类。app.py 中 app.config.from_object(Config) 会读取这里。"""

    # SECRET_KEY 用于 session 和 CSRF 加密。
    SECRET_KEY = os.environ.get('SECRET_KEY', 'photo-manage-platform-dev-key')

    # SQLAlchemy 数据库连接串；默认连接本地 MySQL，可通过 DATABASE_URL 覆盖。
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        DEFAULT_DATABASE_URL
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    MAX_IMAGE_SIZE = int(os.environ.get('MAX_IMAGE_SIZE', 20 * 1024 * 1024))

    # OSS 配置用于图片上传到阿里云对象存储。
    OSS_ENABLED = os.environ.get('OSS_ENABLED', 'true').lower() not in ('0', 'false', 'no')
    OSS_ACCESS_KEY_ID = os.environ.get('OSS_ACCESS_KEY_ID', '')
    OSS_ACCESS_KEY_SECRET = os.environ.get('OSS_ACCESS_KEY_SECRET', '')
    OSS_ENDPOINT = os.environ.get('OSS_ENDPOINT', 'oss-cn-wuhan-lr.aliyuncs.com')
    OSS_BUCKET_NAME = os.environ.get('OSS_BUCKET_NAME', 'photo-manage-oss')
    OSS_UPLOAD_PREFIX = os.environ.get('OSS_UPLOAD_PREFIX', 'photo-manage-platform')
    OSS_BUCKET_DOMAIN = os.environ.get(
        'OSS_BUCKET_DOMAIN',
        'photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com',
    )
