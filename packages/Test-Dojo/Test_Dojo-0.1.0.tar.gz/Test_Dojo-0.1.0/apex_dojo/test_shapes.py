from math import pi

from dataclasses import dataclass
from typing import Protocol


@dataclass
class UnknownShape:
    _area: int

    def area(self) -> int:
        return self._area


@dataclass
class CartesianRectangle:
    x1: int
    x2: int
    y1: int
    y2: int

    def area(self) -> float:
        return (self.x2 - self.x1) * (self.y2 - self.y1)


@dataclass
class Rectangle:
    width: int
    height: int

    def area(self) -> int:
        return self.height * self.width

    def perimeter(self) -> int:
        return 2 * (self.height + self.width)


@dataclass
class Circle:
    radius: int

    def perimeter(self):
        return 2 * self.radius * pi

    def area(self):
        return self.radius**2 * pi


class Shape(Protocol):
    def area(self) -> float:
        pass


@dataclass
class Land:
    shape: Shape

    def calculate_price(self, with_rate: int) -> float:
        return self.shape.area() * with_rate


def test() -> None:
    rectangle = Rectangle(width=2, height=5)
    assert rectangle.perimeter() == 14
    assert rectangle.area() == 10
    assert Land(rectangle).calculate_price(with_rate=2) == 20

    shape = CartesianRectangle(x1=2, x2=4, y1=1, y2=6)
    assert Land(shape).calculate_price(with_rate=2) == 20

    circle = Circle(radius=4)
    assert circle.perimeter() == 8 * pi
    assert circle.area() == 16 * pi
    assert Land(circle).calculate_price(with_rate=2) == 32 * pi

    unknown_shape = UnknownShape(10)
    assert Land(unknown_shape).calculate_price(with_rate=2) == 20
