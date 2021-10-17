import base64
from typing import Callable, AsyncGenerator
from aiohttp import web
from aiohttp.web_middlewares import normalize_path_middleware
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

from config import Config, DatabaseConfig
from handlers import routes
from repository import Repository


def cleanup_database(
    config: DatabaseConfig
) -> Callable[[web.Application], AsyncGenerator]:
    async def cleanup(app: web.Application):
        async with Repository(config) as repository:
            app['repository'] = repository
            yield
    return cleanup


def get_app(config: Config):
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)

    app = web.Application(
        middlewares=[
            normalize_path_middleware(),
            session_middleware(EncryptedCookieStorage(secret_key))
        ],

    )
    app.cleanup_ctx.append(cleanup_database(config.db))
    app['secret_table'] = config.app.secret_table
    app.add_routes(routes)
    return app
