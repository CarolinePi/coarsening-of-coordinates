from typing import Callable, AsyncGenerator, Iterator
from aiohttp import web
from aiohttp.web_middlewares import normalize_path_middleware
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from config import Config, DatabaseConfig
from api.handlers import routes
from dl.repository import Repository


def cleanup_database(
    config: DatabaseConfig
) -> Callable[[web.Application], AsyncGenerator]:
    async def cleanup(app: web.Application) -> AsyncGenerator:
        async with Repository(config) as repository:
            app['repository'] = repository
            yield
    return cleanup


def get_app(config: Config) -> web.Application:
    app = web.Application(
        middlewares=[
            normalize_path_middleware(),
            session_middleware(EncryptedCookieStorage(
                b'Thirty  two  length  bytes  key.')
            )
        ],

    )
    app.cleanup_ctx.append(cleanup_database(config.db))
    app['secret_table'] = config.app.secret_table
    app.add_routes(routes)
    return app
