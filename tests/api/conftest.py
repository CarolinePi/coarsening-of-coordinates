from unittest import mock

import pytest as pytest
from aiohttp import web
from aiohttp.test_utils import TestClient

from api.app import get_app
from config import get_config


@pytest.fixture
async def client_without_login(aiohttp_client) -> TestClient:
    app = get_app(get_config())
    client = await aiohttp_client(app)
    return client


@pytest.fixture
async def client_with_login(aiohttp_client) -> TestClient:
    async def authentication(application: web.Application):
        with mock.patch('api.auth.get_session') as session_mock:
            session_mock.return_value = {'user_id': 1}
            yield

    app = get_app(get_config())
    app.cleanup_ctx.append(authentication)

    client = await aiohttp_client(app)
    return client
