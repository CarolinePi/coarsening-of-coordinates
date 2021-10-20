from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from models_db.base_model import BaseModel
from models_db.location import LocationModel


class UserModel(BaseModel):
    __tablename__ = 'user'

    full_name = Column(String(30), nullable=False)
    password_hash = Column(String(255), nullable=False, unique=True)
    is_admin = Column(Boolean(25), nullable=False)
    location_id = Column(Integer, ForeignKey(LocationModel.id))
    location = relationship(LocationModel)
