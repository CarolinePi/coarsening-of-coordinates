from sqlalchemy import Column, DECIMAL

from models_db.base_model import BaseModel


class LocationModel(BaseModel):
    __tablename__ = 'location'

    # TODO: Validate latitude and longitude by degrees
    latitude = Column(DECIMAL, nullable=False)
    longitude = Column(DECIMAL, nullable=False)

