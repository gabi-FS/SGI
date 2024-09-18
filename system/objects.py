from abc import ABC, abstractmethod

import numpy as np

from globals import ObjectType
from system.basics import Point


class GraphicObject(ABC):
    _id_increment = 1

    _id = int
    _name: str
    _points: list[Point]  # lista de pontos (conjuntos de coordenadas x e y)
    _center: Point
    _type: ObjectType
    _color: tuple

    def __init__(self, name: str, points: list, color) -> None:
        self._id = GraphicObject._id_increment
        GraphicObject._id_increment += 1
        self._name = name
        self._points = points
        self._color = color
        self.compute_center()

    @property
    def id(self):
        return self._id

    @property
    def points(self) -> list[Point]:
        return self._points

    @property
    def center(self) -> Point:
        return self._center

    @abstractmethod
    def draw(self, context, viewport_transform):
        raise NotImplementedError

    def draw_line(self, context, point1: Point, point2: Point):
        context.set_source_rgb(*self._color)
        context.set_line_width(2)
        context.move_to(point1.x, point1.y)
        context.line_to(point2.x, point2.y)
        context.stroke()

    def compute_center(self) -> Point:
        x_list = []
        y_list = []
        for p in self._points:
            x_list.append(p.x)
            y_list.append(p.y)

        center_x = np.mean(x_list)
        center_y = np.mean(y_list)

        self._center = Point(center_x, center_y)

        return self._center

    def update_points(self, new_points: list[Point]):
        self._points = new_points
        self.compute_center()


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
