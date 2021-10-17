import hashlib
import os
from typing import Optional

from aiohttp import web
from aiohttp_session import get_session


def login_required():
    pass


def admin_required():
    pass


async def get_user_in_session(request: web.Request) -> Optional[int]:
    session = await get_session(request)
    return session.get('user_id')


def hash_password(password: str) -> str:
    salt = os.urandom(16).hex().encode('utf-8')
    password_hash = hashlib.pbkdf2_hmac(
        'sha512', password.encode('utf-8'), salt, 100000
    )
    password_hash = password_hash.hex().encode('utf-8')
    return (salt + password_hash).decode('utf-8')


def verify_password(real_password: str, password: str) -> bool:
    salt = real_password[:32].encode('utf-8')
    password_hash = hashlib.pbkdf2_hmac(
        'sha512', password.encode('utf-8'), salt, 100000
    )
    password_hash = password_hash.hex()
    return password_hash == real_password[32:]
