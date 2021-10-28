from decimal import Decimal
from typing import Dict, Any

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer

Base = declarative_base()


class ModelException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return f'Model error: {self.message}'


class BaseModel(Base):    # type: ignore
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

    def as_dict(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    async def check_types(cls, data: Dict[str, Any]) -> None:
        for key, value in data.items():
            column = cls.__table__.columns.get(key)

            if column is None:
                raise ModelException(f'Field {key} doesn`t exits')

            if not column.nullable and value is None:
                raise ModelException(f'Field {key} can`t be null')

            if column.nullable and value is None:
                continue

            field_type = cls.__table__.columns[key].type.python_type
            if not isinstance(value, field_type):
                if not (field_type == Decimal and isinstance(value, float)):
                    raise ModelException(
                        f'Creation model error: Type {field_type} for a '
                        f'field {key} with value {value} and '
                        f'type {type(value)} is not right'
                    )

    def __repr__(self) -> str:
        try:
            return f'<{type(self).__name__} id = {self.id}>'
        except NameError:
            raise ModelException('You need to inherit from Model')
