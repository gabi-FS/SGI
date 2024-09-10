from abc import ABC, abstractmethod

from globals import ObjectType
from system.basics import Point


class GraphicObject(ABC):
    _name: str
    _points: list[Point]  # lista de pontos (conjuntos de coordenadas x e y)
    _center: tuple[Point]
    _type: ObjectType
    _color: tuple

    def __init__(self, name: str, points: list, color) -> None:
        self._name = name
        self._points = points
        self._color = color

    @property
    def points(self):
        return self._points

    @abstractmethod
    def draw(self, context, viewport_transform):
        raise NotImplementedError

    def draw_line(self, context, point1: Point, point2: Point):
        context.set_source_rgb(*self._color)
        context.set_line_width(2)
        context.move_to(point1.x, point1.y)
        context.line_to(point2.x, point2.y)
        context.stroke()


class PointObject(GraphicObject):
    def __init__(self, name: str, points: list, color) -> None:
        super().__init__(name, points, color)
        self._type = ObjectType.POINT

    def draw(self, context, viewport_transform):
        new_point = viewport_transform(self._points[0])
        second_point = Point(new_point.x + 1, new_point.y + 1)
        super().draw_line(context, new_point, second_point)


class LineSegmentObject(GraphicObject):
    def __init__(self, name: str, points: list, color) -> None:
        super().__init__(name, points, color)
        self._type = ObjectType.LINE

    def draw(self, context, viewport_transform):
        initial_point = viewport_transform(self._points[0])
        end_point = viewport_transform(self._points[1])
        super().draw_line(context, initial_point, end_point)


class WireframeObject(GraphicObject):

    def __init__(self, name: str, points: list, color) -> None:
        super().__init__(name, points, color)
        self._type = ObjectType.POLYGON

    def draw(self, context, viewport_transform):
        first_point, *others = self._points
        new_first_point = viewport_transform(first_point)

        for point in others:
            end_point = viewport_transform(point)
            super().draw_line(context, new_first_point, end_point)
            new_first_point = end_point

        new_end_point = viewport_transform(self._points[0])
        super().draw_line(context, new_first_point, new_end_point)
