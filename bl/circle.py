from decimal import Decimal
from typing import Optional


class Circle:
    def __init__(
        self,
        n: Decimal,
        x0: Decimal,
        y0: Decimal,
        x: Optional[Decimal] = None,
        y: Optional[Decimal] = None,
    ):
        self.n = n
        self._x = x
        self._y = y
        self.x0 = x0
        self.y0 = y0

    @property
    def x(self) -> Decimal:
        if self._x is None:
            return Decimal(
                (self.n * self.n - (self.y - self.y0) ** 2).sqrt() + self.x0
            ).quantize(Decimal('0.00001'))
        return self._x

    @property
    def y(self) -> Decimal:
        if self._y is None:
            return Decimal(
                (self.n * self.n - (self.x - self.x0) ** 2).sqrt() + self.y0
            ).quantize(Decimal('0.00001'))
        return self._y
