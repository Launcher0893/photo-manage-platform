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

    # Aliyun OSS test config. Replace these values with your teammate's bucket info.
    OSS_ENABLED = True
    OSS_ACCESS_KEY_ID = 'LTAI5t7E9ZxDJ6ZgwihSbDcU'
    OSS_ACCESS_KEY_SECRET = 'xlmUFVv8tbhR0mv35mSpem8rJbWqKU'
    OSS_ENDPOINT = 'oss-cn-wuhan-lr.aliyuncs.com'
    OSS_BUCKET_NAME = 'photo-manage-oss'
    OSS_UPLOAD_PREFIX = 'photo-manage-platform'
    OSS_BUCKET_DOMAIN = 'photo-manage-oss.oss-cn-wuhan-lr.aliyuncs.com'
