"""图片上传和删除工具。

项目中用户头像、作品图片、帖子图片、公告封面、轮播图都通过这里处理。
整体流程：
1. 校验是否是允许的图片格式。
2. 校验文件大小。
3. 保存到 static/uploads/<folder>/。
4. 如果开启 OSS，再上传到阿里云 OSS。
5. 返回图片 URL，业务代码保存到数据库。
"""

from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Optional
from uuid import uuid4

from flask import current_app, url_for
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from utils.oss_utils import (
    build_oss_object_key,
    extract_object_key_from_url,
    object_key_to_upload_relative_path,
    oss_enabled,
    upload_file_to_oss,
    delete_file_from_oss,
)


ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}


@dataclass
class UploadResult:
    """上传结果对象。

    url：最终给页面使用的图片地址，可能是本地 static 地址，也可能是 OSS 地址。
    filename：生成后的安全文件名。
    local_path：本地保存路径。
    oss_object_name：OSS 中的对象 key，删除 OSS 文件时要用。
    """
    url: str
    filename: str
    local_path: Path
    oss_object_name: Optional[str] = None


def allowed_image(filename: str) -> bool:
    """判断上传文件扩展名是否属于允许的图片格式。"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def save_image_result(file: Optional[FileStorage], folder: str) -> Optional[UploadResult]:
    """保存图片并返回完整上传结果。

    folder 用来区分业务目录，例如：
    - works：作品图片
    - forum：帖子图片
    - avatars：头像
    - announcements：公告封面
    - carousels：轮播图

    被 views/work.py、views/forum.py、views/user.py 等模块调用。
    """
    if file is None or not file.filename:
        return None
    if not allowed_image(file.filename):
        raise ValueError('Only image files are allowed.')
    max_size = int(current_app.config.get('MAX_IMAGE_SIZE', 50 * 1024 * 1024))
    file.stream.seek(0, 2)
    file_size = file.stream.tell()
    file.stream.seek(0)
    if max_size > 0 and file_size > max_size:
        raise ValueError(f'Image file must not exceed {max_size // 1024 // 1024}MB.')

    # secure_filename 会把用户上传的原始文件名处理成安全文件名，避免路径穿越等问题。
    original_name = secure_filename(file.filename)
    suffix = original_name.rsplit('.', 1)[1].lower()
    filename = f'{uuid4().hex}.{suffix}'

    # current_app.static_folder 是 Flask 当前应用的 static 目录。
    upload_root = Path(current_app.static_folder) / 'uploads' / folder
    upload_root.mkdir(parents=True, exist_ok=True)
    local_path = upload_root / filename
    file.save(local_path)

    # url_for('static', ...) 会生成 /static/uploads/... 这样的访问地址。
    local_url = url_for('static', filename=f'uploads/{folder}/{filename}')
    if not oss_enabled():
        return UploadResult(url=local_url, filename=filename, local_path=local_path)

    # object_key 是 OSS 里的文件路径，例如 photo-manage-platform/works/xxx.jpg。
    object_key = build_oss_object_key(folder, filename)
    try:
        oss_url = upload_file_to_oss(local_path, object_key)
    except Exception as exc:
        try:
            local_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise ValueError(str(exc)) from exc

    return UploadResult(
        url=oss_url,
        filename=filename,
        local_path=local_path,
        oss_object_name=object_key,
    )


def save_image(file: Optional[FileStorage], folder: str) -> Optional[str]:
    """保存图片，只返回 URL。

    适合只需要保存图片地址的场景，例如头像、公告封面、轮播图。
    如果业务还需要 oss_object_name，就使用 save_image_result()。
    """
    result = save_image_result(file, folder)
    return result.url if result else None


def _delete_local_static_file(static_relative_path: Optional[str]) -> bool:
    """删除 static/uploads 下的本地副本。

    只允许删除 static/uploads 里的文件，避免误删项目其他文件。
    """
    if not static_relative_path:
        return True

    relative = PurePosixPath(static_relative_path.strip().lstrip('/'))
    if relative.parts and relative.parts[0] == 'static':
        relative = PurePosixPath(*relative.parts[1:])
    if not relative.parts or relative.parts[0] != 'uploads':
        return True

    target = (Path(current_app.static_folder) / Path(*relative.parts)).resolve()
    static_root = Path(current_app.static_folder).resolve()
    try:
        target.relative_to(static_root)
    except ValueError:
        return False

    try:
        target.unlink(missing_ok=True)
        return True
    except OSError:
        return False


def delete_uploaded_file(file_url: Optional[str] = None, oss_object_name: Optional[str] = None) -> bool:
    """删除上传文件。

    同时兼容两种情况：
    - 传入 OSS object key，删除 OSS 文件和对应本地副本。
    - 传入本地 /static/uploads/... URL，删除本地文件。
    """
    ok = True

    object_key = oss_object_name or extract_object_key_from_url(file_url)
    if object_key:
        ok = delete_file_from_oss(object_key) and ok
        ok = _delete_local_static_file(object_key_to_upload_relative_path(object_key)) and ok

    if file_url:
        parsed_path = file_url.split('?', 1)[0]
        ok = _delete_local_static_file(parsed_path) and ok

    return ok
