"""阿里云 OSS 工具。

OSS 可以理解成“云端图片文件夹”。
业务代码不会直接调用 oss2，而是通过本文件封装：
- 生成 OSS 文件路径 object_key。
- 上传本地文件到 OSS。
- 根据 object_key 构造可访问 URL。
- 删除 OSS 文件。
- 从 URL 反推出 object_key。
"""

from pathlib import PurePosixPath
from typing import Optional
from urllib.parse import unquote, urlparse

from flask import current_app


def oss_enabled() -> bool:
    """读取配置，判断是否启用 OSS 上传。"""
    return bool(current_app.config.get('OSS_ENABLED'))


def _clean_path_part(value: str) -> str:
    """清理路径片段，去掉首尾空格和斜杠。"""
    return str(value or '').strip().strip('/\\')


def get_oss_bucket():
    """创建 OSS bucket 对象。

    bucket 可以理解成一个云端存储桶。
    上传和删除文件都要先拿到 bucket。
    """
    try:
        import oss2
    except ImportError as exc:
        raise RuntimeError('oss2 is not installed. Please install it with: pip install oss2') from exc

    access_key_id = current_app.config.get('OSS_ACCESS_KEY_ID')
    access_key_secret = current_app.config.get('OSS_ACCESS_KEY_SECRET')
    endpoint = current_app.config.get('OSS_ENDPOINT')
    bucket_name = current_app.config.get('OSS_BUCKET_NAME')

    missing = [
        name for name, value in (
            ('OSS_ACCESS_KEY_ID', access_key_id),
            ('OSS_ACCESS_KEY_SECRET', access_key_secret),
            ('OSS_ENDPOINT', endpoint),
            ('OSS_BUCKET_NAME', bucket_name),
        )
        if not value or str(value).startswith('YOUR_')
    ]
    if missing:
        raise RuntimeError(f'Missing OSS config: {", ".join(missing)}')

    auth = oss2.Auth(access_key_id, access_key_secret)
    return oss2.Bucket(auth, endpoint, bucket_name)


def build_oss_object_key(folder: str, filename: str) -> str:
    """拼出 OSS 中的文件路径。

    例如 prefix=photo-manage-platform，folder=works，filename=a.jpg，
    最终得到 photo-manage-platform/works/a.jpg。
    """
    prefix = _clean_path_part(current_app.config.get('OSS_UPLOAD_PREFIX', ''))
    folder = _clean_path_part(folder)
    filename = _clean_path_part(filename)
    parts = [part for part in (prefix, folder, filename) if part]
    return str(PurePosixPath(*parts))


def get_oss_base_url() -> str:
    """获取 OSS 访问域名。"""
    domain = str(current_app.config.get('OSS_BUCKET_DOMAIN') or '').strip().rstrip('/')
    if domain:
        if domain.startswith('http://') or domain.startswith('https://'):
            return domain
        return f'https://{domain}'

    bucket_name = current_app.config.get('OSS_BUCKET_NAME')
    endpoint = str(current_app.config.get('OSS_ENDPOINT') or '').strip().lstrip('/')
    if not bucket_name or str(bucket_name).startswith('YOUR_') or not endpoint:
        raise RuntimeError('Missing OSS_BUCKET_NAME or OSS_ENDPOINT')
    return f'https://{bucket_name}.{endpoint}'


def build_oss_url(object_key: str) -> str:
    """把 object_key 拼成浏览器可以访问的完整 URL。"""
    return f'{get_oss_base_url()}/{object_key.lstrip("/")}'


def upload_file_to_oss(local_file_path, object_key: str) -> str:
    """把本地文件上传到 OSS，并返回可访问 URL。"""
    try:
        bucket = get_oss_bucket()
        bucket.put_object_from_file(object_key, str(local_file_path))
        return build_oss_url(object_key)
    except Exception as exc:
        raise RuntimeError(f'OSS upload failed: {exc}') from exc


def delete_file_from_oss(object_key: Optional[str]) -> bool:
    """删除 OSS 上的文件。

    删除失败时返回 False，业务层可以据此提示“图片删除失败”。
    """
    if not object_key or not oss_enabled():
        return True
    try:
        bucket = get_oss_bucket()
        bucket.delete_object(object_key)
        return True
    except Exception:
        return False


def extract_object_key_from_url(file_url: Optional[str]) -> Optional[str]:
    """从 OSS URL 中提取 object_key。

    例如 https://bucket.endpoint/photo-manage-platform/works/a.jpg
    提取出 photo-manage-platform/works/a.jpg。
    """
    if not file_url:
        return None

    parsed = urlparse(file_url)
    if not parsed.scheme or not parsed.netloc:
        return None

    try:
        base = urlparse(get_oss_base_url())
    except RuntimeError:
        return None
    if parsed.netloc.lower() != base.netloc.lower():
        return None

    path = unquote(parsed.path).lstrip('/')
    return path or None


def object_key_to_upload_relative_path(object_key: Optional[str]) -> Optional[str]:
    """把 OSS object_key 转成 static/uploads 下的本地相对路径。

    用于删除 OSS 文件时同步删除本地保存的副本。
    """
    if not object_key:
        return None

    key = object_key.strip().lstrip('/')
    prefix = _clean_path_part(current_app.config.get('OSS_UPLOAD_PREFIX', ''))
    if prefix and key.startswith(f'{prefix}/'):
        key = key[len(prefix) + 1:]

    parts = [part for part in PurePosixPath(key).parts if part not in ('', '.', '..')]
    if len(parts) < 2:
        return None
    return str(PurePosixPath('uploads', *parts))
