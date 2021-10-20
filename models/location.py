from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Location:
    latitude: Decimal  # X
    longitude: Decimal  # y
