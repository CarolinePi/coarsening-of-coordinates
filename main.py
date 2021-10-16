from decimal import Decimal

from circle import Circle
from enums import Sign, Axis
from hash_function import HashFunction
from models import User, Location
from random import shuffle

if __name__ == '__main__':
    # example_table = [i for i in range(1, 181)]
    # shuffle(example_table)
    # print(example_table)
    example_table = [146, 172, 30, 158, 169, 130, 62, 91, 94, 112, 63, 164, 124, 11, 7, 144, 33, 74, 99, 39, 147, 151, 50, 79, 145, 1, 108, 156, 60, 21, 29, 157, 52, 45, 152, 116, 165, 73, 180, 93, 142, 87, 95, 160, 41, 137, 14, 140, 118, 97, 64, 126, 6, 68, 44, 55, 18, 100, 16, 125, 19, 103, 148, 17, 134, 37, 131, 111, 82, 43, 32, 23, 98, 106, 175, 49, 65, 10, 174, 133, 25, 34, 163, 51, 143, 115, 12, 176, 173, 67, 121, 66, 177, 84, 128, 155, 138, 4, 110, 3, 53, 135, 80, 36, 81, 120, 119, 42, 168, 117, 69, 46, 31, 35, 71, 88, 58, 70, 105, 28, 139, 178, 54, 104, 166, 86, 5, 57, 129, 127, 102, 101, 170, 40, 171, 132, 76, 109, 136, 85, 92, 61, 179, 26, 24, 78, 72, 107, 153, 75, 113, 114, 48, 83, 2, 89, 159, 47, 56, 150, 167, 149, 154, 15, 27, 122, 8, 13, 161, 77, 9, 38, 20, 162, 59, 22, 141, 123, 96, 90]

    # user = User(
    #     full_name='Caroline Pospelova',
    #     user_id='111',
    #     location=Location(
    #         lat=Decimal(123.2987).quantize(Decimal('0.00001')),
    #         lon=Decimal(34.5454545).quantize(Decimal('0.00001')),
    #     )
    # )
    #
    # hash_function = HashFunction(example_table)
    # a = hash_function.create_hash(user.full_name)
    # a = Decimal(a / 10000).quantize(Decimal('0.00001'))
    # print(a)
    #
    # axis = user.choose_coordinate_axis_for_start()
    # if axis == Axis.X:
    #     value = (
    #         user.location.lat + a
    #         if user.choose_sign() == Sign.POSITIVE
    #         else 0 - a + user.location.lat
    #     )
    # if axis == Axis.Y:
    #     value = (
    #         user.location.lon + a
    #         if user.choose_sign() == Sign.POSITIVE
    #         else 0 - a + user.location.lon
    #     )
    # addition_param = {axis.value: value.quantize(Decimal('0.00001'))}
    #
    # circle = Circle(
    #     n=Decimal(0.018),
    #     x0=user.location.lat,
    #     y0=user.location.lon,
    #     **addition_param
    # )
    # print(addition_param)
    # print(circle.x)
    # print(circle.y)

    from aiohttp import web

    from app import get_app
    from config import get_config

    app = get_app(get_config())
    web.run_app(app)

