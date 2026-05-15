from pathlib import PurePosixPath
from typing import Optional
from urllib.parse import unquote, urlparse

from flask import current_app


def oss_enabled() -> bool:
    return bool(current_app.config.get('OSS_ENABLED'))


def _clean_path_part(value: str) -> str:
    return str(value or '').strip().strip('/\\')


def get_oss_bucket():
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
    prefix = _clean_path_part(current_app.config.get('OSS_UPLOAD_PREFIX', ''))
    folder = _clean_path_part(folder)
    filename = _clean_path_part(filename)
    parts = [part for part in (prefix, folder, filename) if part]
    return str(PurePosixPath(*parts))


def get_oss_base_url() -> str:
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
    return f'{get_oss_base_url()}/{object_key.lstrip("/")}'


def upload_file_to_oss(local_file_path, object_key: str) -> str:
    try:
        bucket = get_oss_bucket()
        bucket.put_object_from_file(object_key, str(local_file_path))
        return build_oss_url(object_key)
    except Exception as exc:
        raise RuntimeError(f'OSS upload failed: {exc}') from exc


def delete_file_from_oss(object_key: Optional[str]) -> bool:
    if not object_key or not oss_enabled():
        return True
    try:
        bucket = get_oss_bucket()
        bucket.delete_object(object_key)
        return True
    except Exception:
        return False


def extract_object_key_from_url(file_url: Optional[str]) -> Optional[str]:
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
