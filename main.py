from aiohttp import web

from app import get_app
from config import get_config

app = get_app(get_config())
web.run_app(app)

