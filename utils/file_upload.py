from pathlib import Path
from uuid import uuid4

from flask import current_app, url_for
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}


def allowed_image(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def save_image(file: FileStorage | None, folder: str) -> str | None:
    if file is None or not file.filename:
        return None
    if not allowed_image(file.filename):
        raise ValueError('Only image files are allowed.')

    original_name = secure_filename(file.filename)
    suffix = original_name.rsplit('.', 1)[1].lower()
    filename = f'{uuid4().hex}.{suffix}'

    upload_root = Path(current_app.static_folder) / 'uploads' / folder
    upload_root.mkdir(parents=True, exist_ok=True)
    file.save(upload_root / filename)

    return url_for('static', filename=f'uploads/{folder}/{filename}')
