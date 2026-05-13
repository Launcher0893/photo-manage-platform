import hashlib


def md5_encrypt(password):
    raw = '' if password is None else str(password)
    return hashlib.md5(raw.encode('utf-8')).hexdigest()


def is_md5_hash(value):
    if not isinstance(value, str) or len(value) != 32:
        return False
    return all(char in '0123456789abcdefABCDEF' for char in value)


def verify_password(stored_password, raw_password):
    if stored_password is None:
        return False

    stored = str(stored_password)
    hashed = md5_encrypt(raw_password)
    if stored.lower() == hashed:
        return True

    # Compatibility for old seed data that was inserted as plain text.
    return not is_md5_hash(stored) and stored == str(raw_password)


def password_needs_upgrade(stored_password, raw_password):
    if stored_password is None:
        return False
    stored = str(stored_password)
    return not is_md5_hash(stored) and stored == str(raw_password)
