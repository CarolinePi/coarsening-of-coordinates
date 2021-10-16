from aiohttp import web
from aiohttp_session import get_session, new_session

from auth import hash_password

routes = web.RouteTableDef()


@routes.get('/healthcheck')
async def healthcheck(request: web.Request) -> web.Response:
    return web.HTTPOk(text='I am fine!')


@routes.get('/example')
async def example(request: web.Request) -> web.Response:
    print(request.app['secret_table'])
    print(request.cookies)
    return web.HTTPOk(text='I am fine!')


@routes.post('/register')
async def register(request: web.Request) -> web.Response:
    data = await request.json()
    user_id = 1

    hash_password(data['password'])

    session = await new_session(request)
    session['user_id'] = str(user_id)
    return web.HTTPOk(text='You are register')


@routes.post('/login')
async def login(request: web.Request) -> web.Response:
    # TODO
    return web.HTTPOk(text='You logout')


@routes.post('logout')
async def logout(request: web.Request) -> web.Response:
    session = await get_session(request)
    session.invalidate()
    return web.HTTPOk(text='You logout')
