import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_DATABASE_URL = (
    'mysql+pymysql://root:Sean20041218@127.0.0.1:3306/'
    'photo_manage_platform?charset=utf8mb4'
)


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'photo-manage-platform-dev-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        DEFAULT_DATABASE_URL
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    MAX_IMAGE_SIZE = int(os.environ.get('MAX_IMAGE_SIZE', 5 * 1024 * 1024))

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
