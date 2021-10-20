from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer

Base = declarative_base()


class ModelException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f'Model error: {self.message}'


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        try:
            return f'<{type(self).__name__} id = {self.id}>'
        except NameError:
            raise ModelException(f'You need to inherit from Model')
