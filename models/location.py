from sqlalchemy import Column, DECIMAL

from models.base_model import BaseModel


class LocationModel(BaseModel):
    __tablename__ = 'location'

    # TODO: Validate lat and lon by degrees
    latitude = Column(DECIMAL, nullable=False)
    longitude = Column(DECIMAL, nullable=False)

