from decimal import Decimal
from typing import List

from circle import Circle
from enums import Axis, Sign
from hash_function import HashFunction
from models.location import Location
from models.user import User


def get_user_location(secret_table: List[int], user: User):
    hash_function = HashFunction(secret_table)
    hash_for_first_axis = hash_function.create_hash(user.full_name)
    first_axis = Decimal(hash_for_first_axis / 10000).quantize(Decimal('0.00001'))

    axis = user.choose_coordinate_axis_for_start()
    if axis == Axis.X:
        value = _get_value(
            first_axis, user.choose_sign(), user.location.latitude
        )
    elif axis == Axis.Y:
        value = _get_value(
            first_axis, user.choose_sign(), user.location.longitude
        )

    addition_param = {axis.value: value.quantize(Decimal('0.00001'))}
    circle = Circle(
        n=Decimal(0.018),   # TODO: go to config
        x0=user.location.latitude,
        y0=user.location.longitude,
        **addition_param
    )
    return Location(latitude=circle.x, longitude=circle.y)


def _get_value(
    first_axis: Decimal, sign: Sign, location_coordinate: Decimal
) -> Decimal:
    return (
        location_coordinate + first_axis
        if sign == Sign.POSITIVE
        else 0 - first_axis + location_coordinate
    )


class DecimalSerializationDict(dict):
    def __init__(self, data):
        super().__init__(
            (k, str(v)) if isinstance(v, Decimal) else (k, v)
            for (k, v) in data
        )