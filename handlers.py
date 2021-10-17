from aiohttp import web
from aiohttp_session import get_session, new_session

from auth import hash_password, get_user_in_session, verify_password
from model import User
from models.location import LocationModel
from models.user import UserModel

routes = web.RouteTableDef()


@routes.get('/healthcheck')
async def healthcheck(request: web.Request) -> web.Response:
    return web.HTTPOk(text='I am fine!')


@routes.get('/user')
async def example(request: web.Request) -> web.Response:
    print(request.app['secret_table'])
    print(request.cookies)
    return web.HTTPOk(text='I am fine!')


@routes.post('/register')
async def register(request: web.Request) -> web.Response:
    user_id = await get_user_in_session(request)
    if user_id:
        return web.HTTPForbidden(text='You already registered')

    data = await request.json()

    location_id = await request.app['repository'].insert_row_to_model(
        model=LocationModel, **data['location']
    )

    user_id = await request.app['repository'].insert_row_to_model(
        model=UserModel,
        full_name=data['full_name'],
        password_hash=hash_password(data['password']),
        is_admin=False,
        location_id=location_id,
    )
    session = await new_session(request)
    session['user_id'] = str(user_id)
    return web.HTTPOk(text='You registered')


@routes.post('/login')
async def login(request: web.Request) -> web.Response:
    user_id = await get_user_in_session(request)
    if user_id:
        return web.HTTPForbidden(text='You already signed in')

    data = await request.json()
    real_password = await request.app['repository'].select_user_password(
        data['full_name']
    )

    if verify_password(real_password, data['password']):
        session = await new_session(request)
        session['user_id'] = str(user_id)
        return web.HTTPOk(text='You login')
    else:
        return web.HTTPUnauthorized(text='Password or login is invalid')


@routes.post('/logout')
async def logout(request: web.Request) -> web.Response:
    session = await get_session(request)
    session.invalidate()
    return web.HTTPOk(text='You logout')
