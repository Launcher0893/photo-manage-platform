from dataclasses import dataclass
from pathlib import Path, PurePosixPath
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
    url: str
    filename: str
    local_path: Path
    oss_object_name: str | None = None


def allowed_image(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def save_image_result(file: FileStorage | None, folder: str) -> UploadResult | None:
    if file is None or not file.filename:
        return None
    if not allowed_image(file.filename):
        raise ValueError('Only image files are allowed.')

    original_name = secure_filename(file.filename)
    suffix = original_name.rsplit('.', 1)[1].lower()
    filename = f'{uuid4().hex}.{suffix}'

    upload_root = Path(current_app.static_folder) / 'uploads' / folder
    upload_root.mkdir(parents=True, exist_ok=True)
    local_path = upload_root / filename
    file.save(local_path)

    local_url = url_for('static', filename=f'uploads/{folder}/{filename}')
    if not oss_enabled():
        return UploadResult(url=local_url, filename=filename, local_path=local_path)

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


def save_image(file: FileStorage | None, folder: str) -> str | None:
    result = save_image_result(file, folder)
    return result.url if result else None


def _delete_local_static_file(static_relative_path: str | None) -> bool:
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


def delete_uploaded_file(file_url: str | None = None, oss_object_name: str | None = None) -> bool:
    ok = True

    object_key = oss_object_name or extract_object_key_from_url(file_url)
    if object_key:
        ok = delete_file_from_oss(object_key) and ok
        ok = _delete_local_static_file(object_key_to_upload_relative_path(object_key)) and ok

    if file_url:
        parsed_path = file_url.split('?', 1)[0]
        ok = _delete_local_static_file(parsed_path) and ok

    return ok
