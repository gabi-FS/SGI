from enum import Enum


class ObjectType(Enum):
    POINT = 1
    LINE = 2
    POLYGON = 3


class Point:
    _x: float
    _y: float

    def __init__(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __add__(self, other):

        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __iter__(self):
        return iter([self._x, self._y])
