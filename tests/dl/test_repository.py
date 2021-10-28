import random
import string
from decimal import Decimal

import pytest

from dl.models.location import LocationModel
from dl.models.user import UserModel


@pytest.mark.parametrize('model, ids, result', [
    ([UserModel, [1], [(1, 'Caroline Pospelova', 'password', False, 1)]]),
    ([UserModel, [1, 2], [(1, 'Caroline Pospelova', 'password', False, 1), (2, 'Nik Pospelov', 'password2', False, 2)]]),
    ([LocationModel, [1], [(1, Decimal('123.23123'), Decimal('87.323'))]])
])
async def test_select_from_model_by_ids(
    test_db, repository, model, ids, result
):
    data = await repository.select_from_model_by_ids(model, ids)
    assert data == result


async def test_insert_row_to_model_user(repository, test_db):
    password = ''.join(random.choices(string.ascii_lowercase, k=32))

    model = UserModel
    data = {
        'id': 100,
        'full_name': 'Vasya Pupkin',
        'location_id': 1,
        'password_hash': password
    }
    await repository.insert_row_to_model(model, **data)
    data_result = await repository.select_from_model_by_ids(model, [100])
    result = [(100, 'Vasya Pupkin', password, False, 1)]
    assert data_result == result
    await repository.delete_row_to_model_by_id(model, 100)


async def test_insert_row_to_model_location(repository):
    model = LocationModel
    data = {
        'id': 100,
        'latitude': Decimal(123.232432).quantize(Decimal('0.00001')),
        'longitude': Decimal(334.34232).quantize(Decimal('0.00001')),
    }
    await repository.insert_row_to_model(model, **data)
    data_result = await repository.select_from_model_by_ids(model, [100])
    result = [(100, Decimal('123.23243'), Decimal('334.34232'))]
    assert data_result == result
    await repository.delete_row_to_model_by_id(model, 100)


async def test_select_user_full_info_by_id(repository, test_db):
    data_result = await repository.select_user_full_info_by_id(1)
    result = (1, 'Caroline Pospelova', Decimal('87.323'), Decimal('123.23123'))
    assert data_result == result
