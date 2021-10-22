import pytest

from bl.hash_function import HashFunction


@pytest.mark.parametrize('secret_table, result', [
    ([2, 1, 3, 5, 7, 4, 6], 4),
    ([2, 1, 3], 2),
    ([7, 5, 2, 1, 9, 8, 3, 10, 6, 4], 7),
])
def test_hash_function(secret_table, result):
    hash_function = HashFunction(secret_table)
    hash_for_first_axis = hash_function.create_hash('Caroline')
    assert hash_for_first_axis == result
