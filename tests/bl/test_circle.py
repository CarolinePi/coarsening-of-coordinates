from decimal import Decimal

from bl.circle import Circle


def test_circle_coordinates_with_start_x():
    x_start = Decimal(123.23733).quantize(Decimal('0.00001'))
    circle = Circle(
        n=Decimal(0.018).quantize(Decimal('0.001')),
        x0=Decimal(123.23123).quantize(Decimal('0.00001')),
        y0=Decimal(2322.323).quantize(Decimal('0.00001')),
        x=x_start,
    )
    assert circle.x == x_start
    assert circle.y == Decimal(2322.33993).quantize(Decimal('0.00001'))


def test_circle_coordinates():
    y_start = Decimal(2322.329).quantize(Decimal('0.00001'))
    circle = Circle(
        n=Decimal(0.018).quantize(Decimal('0.001')),
        x0=Decimal(123.23123).quantize(Decimal('0.00001')),
        y0=Decimal(2322.323).quantize(Decimal('0.00001')),
        y=y_start,
    )
    assert circle.x == Decimal(123.24820).quantize(Decimal('0.00001'))
    assert circle.y == y_start
