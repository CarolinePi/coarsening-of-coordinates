from enum import Enum, auto
from typing import List, Any


class Sign(Enum):
    POSITIVE = auto()
    NEGATIVE = auto()


class AutoNameEnum(Enum):
    def _generate_next_value_(name: str, *args: List[Any]) -> str:    # type: ignore    # noqa
        return name.lower()


class Axis(AutoNameEnum):
    X = auto()
    Y = auto()
