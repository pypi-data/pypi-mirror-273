from __future__ import annotations

import math


class Rectangle:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height

    def __str__(self) -> str:
        return f"Rectangle(width={self.width}, height={self.height})"

    def get_area(self) -> int:
        return self.width * self.height

    def get_perimeter(self) -> int:
        return 2 * (self.width + self.height)

    def get_diagonal(self) -> int | float:
        return math.sqrt(self.width**2 + self.height**2)

    def set_width(self, param: int) -> None:
        self.width = param

    def set_height(self, param: int) -> None:
        self.height = param

    def get_picture(self) -> str:
        if self.width > 50 or self.height > 50:
            return "Too big for picture."

        return "".join(("*" * self.width + "\n") * self.height)

    def get_amount_inside(self, sq: Rectangle) -> int:
        return (self.width // sq.width) * (self.height // sq.height)


class Square(Rectangle):
    def __init__(self, length: int):
        super().__init__(length, length)

    def __str__(self) -> str:
        return f"Square(side={self.width})"

    def set_side(self, param: int) -> None:
        self.width, self.height = param, param
