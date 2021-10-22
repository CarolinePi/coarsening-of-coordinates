from decimal import Decimal

from api.mapping import mapping_user_model_to_user_calculate
from bl.models.location import Location
from bl.utils import get_user_location


async def test_get_user_location(repository):
    user = await repository.select_user_full_info_by_id(
        1
    )
    user_calculate = mapping_user_model_to_user_calculate(user)
    location = get_user_location([5, 7, 2, 8, 4, 1, 3, 6], user_calculate)
    result = Location(
        latitude=Decimal('123.23183'),
        longitude=Decimal('2322.32380')
    )
    assert location == result
