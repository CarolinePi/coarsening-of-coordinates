from aiohttp import web
from aiohttp_session import get_session, new_session
from dataclasses import asdict

from api.auth import (
    hash_password,
    verify_password,
    get_user_in_session
)
from api.mapping import mapping_user_model_to_user_calculate
from dl.models.location import LocationModel
from dl.models.user import UserModel
from bl.utils import get_user_location, DecimalSerializationDict

routes = web.RouteTableDef()


@routes.get('/healthcheck')
async def healthcheck(request: web.Request) -> web.Response:
    return web.HTTPOk(text='I am fine!')


@routes.get('/user/{id}')
async def get_user(request: web.Request) -> web.Response:
    user = await get_user_in_session(request)
    user_id = user.id if user is not None else None
    is_admin = user.is_admin if user is not None else False
    searched_user_id = int(request.match_info['id'])
    searched_user = await request.app['repository'].select_user_full_info_by_id(
        searched_user_id)
    user_calculate = mapping_user_model_to_user_calculate(searched_user)

    if not (is_admin or user_id == searched_user_id):
        location = get_user_location(
            request.app['secret_table'], user_calculate
        )
        user_calculate.location = location

    data = asdict(user_calculate, dict_factory=DecimalSerializationDict)
    return web.json_response(data, status=200)


@routes.post('/register')
async def register(request: web.Request) -> web.Response:
    user = await get_user_in_session(request)
    if user:
        return web.HTTPForbidden(text='You already registered')

    data = await request.json()

    location_id = await request.app['repository'].insert_row_to_model(
        model=LocationModel, **data['location']
    )
    # TODO: do transaction insert location and user
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
    user = await get_user_in_session(request)
    if user:
        return web.HTTPForbidden(text='You already signed in')

    data = await request.json()
    result = await request.app['repository'].select_user_login_data(
        data['full_name']
    )
    if verify_password(result.user_password_hash, data['password']):
        session = await new_session(request)
        session['user_id'] = str(result.user_id)
        return web.HTTPOk(text='You login')
    else:
        return web.HTTPUnauthorized(text='Password or login is invalid')


@routes.post('/logout')
async def logout(request: web.Request) -> web.Response:
    session = await get_session(request)
    session.invalidate()
    return web.HTTPOk(text='You logout')
