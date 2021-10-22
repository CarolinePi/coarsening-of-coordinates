import random
import string
from decimal import Decimal

import pytest

from dl.models.location import LocationModel
from dl.models.user import UserModel


@pytest.mark.parametrize('model, ids, result', [
    ([UserModel, [1], [(1, 'Caroline Pospelova', '7df997f12feb4da169dcaaef7104075434be6b31385028e30b817e9d7316636dbb2061d009e8410871b842105f71862b36d67847ca6a32999368b102aa2c6f96246e536f4852d188385b0e9144b39d51', False, 10)]]),
    ([UserModel, [1, 2], [(1, 'Caroline Pospelova', '7df997f12feb4da169dcaaef7104075434be6b31385028e30b817e9d7316636dbb2061d009e8410871b842105f71862b36d67847ca6a32999368b102aa2c6f96246e536f4852d188385b0e9144b39d51', False, 10), (2, 'Caroline Pospelova', 'a1765e28f4c515135a27f1858905c33203dcb7311062816d934166ad5343a858767d53f5d9eec1dd4242dd39870295b5509acdda921f79145f3011b64bd5a3861f760245bf358bd60ea27dc2f613acaf', False, 11)]]),
    ([LocationModel, [10], [(10, Decimal('123.23123'), Decimal('2322.323'))]])
])
async def test_select_from_model_by_ids(repository, model, ids, result):
    data = await repository.select_from_model_by_ids(model, ids)
    assert data == result


async def test_insert_row_to_model_user(repository):
    password = ''.join(random.choices(string.ascii_lowercase, k=32))

    model = UserModel
    data = {
        'full_name': 'Vasya Pupkin',
        'location_id': 10,
        'password_hash': password
    }
    user_id = await repository.insert_row_to_model(model, **data)
    data_result = await repository.select_from_model_by_ids(model, [user_id])
    result = [(user_id, 'Vasya Pupkin', password, False, 10)]
    assert data_result == result


async def test_insert_row_to_model_location(repository):
    model = LocationModel
    data = {
        'latitude': Decimal(123.232432).quantize(Decimal('0.00001')),
        'longitude': Decimal(334.34232).quantize(Decimal('0.00001')),
    }
    location_id = await repository.insert_row_to_model(model, **data)
    data_result = await repository.select_from_model_by_ids(model, [location_id])
    result = [(location_id, Decimal('123.23243'), Decimal('334.34232'))]
    assert data_result == result


async def test_select_user_full_info_by_id(repository):
    data_result = await repository.select_user_full_info_by_id(1)
    result = (1, 'Caroline Pospelova', Decimal('2322.323'), Decimal('123.23123'))
    assert data_result == result
