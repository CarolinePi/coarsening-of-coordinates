from aiopg.sa.result import RowProxy

from models.location import Location
from models.user import User


def mapping_user_model_to_user_calculate(row: RowProxy) -> User:
    return User(
        id=row.id,
        full_name=row.full_name,
        location=Location(
            longitude=row.longitude,
            latitude=row.latitude,
        )
    )

