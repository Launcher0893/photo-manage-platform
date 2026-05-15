"""密码加密与校验工具。

课程项目中密码使用 MD5 保存。
注意：真实生产系统不建议用 MD5 保存密码，但课程项目中用于演示登录流程。
这里还兼容旧演示数据中的明文密码：如果旧明文登录成功，会在 auth.py 中升级为 MD5。
"""

import hashlib


def md5_encrypt(password):
    """把原始密码转成 32 位 MD5 字符串。"""
    raw = '' if password is None else str(password)
    return hashlib.md5(raw.encode('utf-8')).hexdigest()


def is_md5_hash(value):
    """判断一个字符串看起来是不是 MD5 哈希值。"""
    if not isinstance(value, str) or len(value) != 32:
        return False
    return all(char in '0123456789abcdefABCDEF' for char in value)


def verify_password(stored_password, raw_password):
    """校验用户输入的密码是否正确。

    stored_password 是数据库里的密码。
    raw_password 是登录表单里输入的密码。
    优先按 MD5 校验；如果数据库里不是 MD5，则兼容旧明文密码。
    """
    if stored_password is None:
        return False

    stored = str(stored_password)
    hashed = md5_encrypt(raw_password)
    if stored.lower() == hashed:
        return True

    # Compatibility for old seed data that was inserted as plain text.
    return not is_md5_hash(stored) and stored == str(raw_password)


def password_needs_upgrade(stored_password, raw_password):
    """判断旧明文密码是否需要升级为 MD5。"""
    if stored_password is None:
        return False
    stored = str(stored_password)
    return not is_md5_hash(stored) and stored == str(raw_password)
