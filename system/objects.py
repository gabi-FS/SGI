from abc import ABC
from enum import Enum


class Coordinate:
    _x: int
    _y: int

    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class ObjectType(Enum):
    POINT = 1
    LINE = 2
    POLYGON = 3


class GraphicObject(ABC):
    _name: str
    _coords: list[Coordinate]  # lista de coordenadas
    _center: tuple[Coordinate]
    _type: ObjectType

    def __init__(self, name: str, coords: list) -> None:
        self._name = name
        self._coords = coords

    @property
    def coords(self):
        return self._coords


class Point(GraphicObject):
    def __init__(self, name: str, coords: list) -> None:
        super().__init__(name, coords)
        self._type = ObjectType.POINT


class LineSegment(GraphicObject):
    def __init__(self, name: str, coords: list) -> None:
        super().__init__(name, coords)
        self._type = ObjectType.LINE


class Wireframe(GraphicObject):

    def __init__(self, name: str, coords: list) -> None:
        super().__init__(name, coords)
        self._type = ObjectType.POLYGON
