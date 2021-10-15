from dataclasses import dataclass
from decimal import Decimal
from typing import List

from enums import Sign, Axis


@dataclass
class Location:
    lat: Decimal  # X
    lon: Decimal  # y


@dataclass
class User:
    full_name: str
    user_id: str
    location: Location

    def do_split_full_name(self) -> List[str]:
        return self.full_name.split()

    def choose_sign(self) -> Sign:
        surname = self.do_split_full_name()[0]
        if len(surname) % 2 == 0:
            return Sign.POSITIVE
        return Sign.NEGATIVE

    def choose_coordinate_axis_for_start(self) -> Axis:
        name = self.do_split_full_name()[0]
        if len(name) % 2 == 0:
            return Axis.X
        return Axis.Y
