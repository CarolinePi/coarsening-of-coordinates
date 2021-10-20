import hashlib
import os
from functools import wraps
from typing import Optional, Callable

from aiohttp import web
from aiohttp_session import get_session

from models_db.user import UserModel


def login_required(handler: Callable) -> Callable:
    @wraps(handler)
    async def wrapper(request: web.Request) -> web.Response:
        user_id = await get_user_id_in_session(request)
        if not user_id:
            web.HTTPUnauthorized(text='You must be signed up')
        request['user'] = await (
            request.app['repository'].select_from_model_by_ids([user_id])
        )
        return await handler(request)
    return wrapper


async def get_user_id_in_session(request: web.Request) -> Optional[int]:
    session = await get_session(request)
    return session.get('user_id')


async def get_user_in_session(request: web.Request) -> Optional[UserModel]:
    user_id = await get_user_id_in_session(request)
    print(user_id)
    if not user_id:
        return None
    user = await request.app['repository'].select_from_model_by_ids(
        UserModel, [user_id]
    )
    return user[0] if user else None


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
