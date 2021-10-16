import hashlib
import os


def login_required():
    pass


def admin_required():
    pass


def hash_password(password: str) -> str:
    salt = os.urandom(32).hex().encode('utf-8')
    password_hash = hashlib.pbkdf2_hmac(
        'sha512', password.encode('utf-8'), salt, 100000
    )
    password_hash = password_hash.hex().encode('utf-8')
    return (salt + password_hash).decode('utf-8')


def verify_password(stored_password: str, provided_password: str) -> bool:
    salt = stored_password[:64].encode('utf-8')
    password_hash = hashlib.pbkdf2_hmac(
        'sha512', provided_password.encode('utf-8'), salt, 100000
    )
    password_hash = password_hash.hex()
    return password_hash == stored_password[64:]
