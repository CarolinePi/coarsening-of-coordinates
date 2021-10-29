from aiohttp import web
from aiohttp_apispec import docs, request_schema, response_schema
from aiohttp_session import get_session, new_session
from dataclasses import asdict
from marshmallow import ValidationError

from api.auth import (
    hash_password,
    verify_password,
    get_user_in_session
)
from api.mapping import mapping_user_model_to_user_calculate
from api.schema import RegisterRequestSchema, LoginRequestSchema, \
    GetUserResponseSchema
from dl.models.location import LocationModel
from dl.models.user import UserModel
from bl.utils import get_user_location, DecimalSerializationDict

routes = web.RouteTableDef()


@docs(
    tags=["health"],
    summary="Check if service is working",
    responses={
        200: {"description": "Ok. Server is alive"},
        500: {"description": "Server error, gg wp"},
    },
)
@routes.get('/healthcheck', allow_head=False)
async def healthcheck(request: web.Request) -> web.Response:
    return web.HTTPOk(text='I am fine!')


@docs(
    tags=["user"],
    summary="Test method user",
    responses={
        200: {"description": "Success response",
              "schema": GetUserResponseSchema},
        500: {"description": "Server Error"},
    },
)
@response_schema(GetUserResponseSchema, 200)
@routes.get('/user/{id}', allow_head=False)
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


@docs(
    tags=["auth"],
    summary="Test method register",
    responses={
        200: {"description": "Success registed"},
        403: {"description": "Forbidden"},
        422: {"description": "Validation error"},
    },
)
@request_schema(RegisterRequestSchema())
@routes.post('/register')
async def register(request: web.Request) -> web.Response:
    user = await get_user_in_session(request)
    if user:
        return web.HTTPForbidden(text='You already registered')

    try:
        data = RegisterRequestSchema().load(await request.json())
    except ValidationError as e:
        return web.HTTPUnprocessableEntity(text=str(e.messages))

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
    return web.HTTPOk(text=f'You registered id = {user_id}')


@docs(
    tags=["auth"],
    summary="Test method login",
    responses={
        200: {"description": "Success login"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        422: {"description": "Validation error"},
    },
)
@request_schema(RegisterRequestSchema())
@routes.post('/login')
async def login(request: web.Request) -> web.Response:
    user = await get_user_in_session(request)
    if user:
        return web.HTTPForbidden(text='You already signed in')

    try:
        data = LoginRequestSchema().load(await request.json())
    except ValidationError as e:
        return web.HTTPUnprocessableEntity(text=str(e.messages))

    result = await request.app['repository'].select_user_login_data(
        data['full_name']
    )
    if verify_password(result.user_password_hash, data['password']):
        session = await new_session(request)
        session['user_id'] = str(result.user_id)
        return web.HTTPOk(text='You login')
    else:
        return web.HTTPUnauthorized(text='Password or login is invalid')


@docs(
    tags=["auth"],
    summary="Test method logout",
    responses={
        200: {"description": "Success logout"},
    },
)
@routes.post('/logout')
async def logout(request: web.Request) -> web.Response:
    session = await get_session(request)
    session.invalidate()
    return web.HTTPOk(text='You logout')
