from abc import ABC, abstractmethod
from typing import Callable, List

import cairo

from globals import LineClippingType, ObjectType
from system.basics import Point
from system.clipping import Clipping
from system.files import ObjectDescriptor


class GraphicObject(ABC):
    _id_increment = 1

    _id = int
    _name: str
    _points: list[Point]  # lista de pontos (conjuntos de coordenadas x e y)
    _center: Point
    _type: ObjectType
    _color: tuple
    _normalized_points: list[Point]
    _normalized_center: Point

    def __init__(self, name: str, points: list, color) -> None:
        self._id = GraphicObject._id_increment
        GraphicObject._id_increment += 1
        self._name = name
        self._points = points
        self._color = color
        self._normalized_points = points
        self._normalized_center = self.compute_center()

    @property
    def id(self):
        return self._id

    @property
    def points(self) -> list[Point]:
        return self._points

    @property
    def center(self) -> Point:
        return self._center

    @property
    def type(self) -> ObjectType:
        return self._type

    @property
    def normalized_points(self) -> list[Point]:
        return self._normalized_points

    @property
    def normalized_center(self) -> Point:
        return self._normalized_center

    @abstractmethod
    def draw(
            self,
            context,
            viewport_transform: "function",
            window_min: Point,
            window_max: Point,
            clipping: Clipping
    ):
        raise NotImplementedError

    def draw_line(self, context: cairo.Context, point1: Point, point2: Point):
        context.set_source_rgb(*self._color)
        context.set_line_width(2)
        context.move_to(point1.x, point1.y)
        context.line_to(point2.x, point2.y)
        context.stroke()

    def compute_center(self) -> Point:
        self._center = Point.get_geometric_center(self._points)
        return self._center

    def compute_normalized_center(self) -> Point:
        self._normalized_center = Point.get_geometric_center(self._points)
        return self._normalized_center

    def update_points(self, new_points: list[Point]):
        self._points = new_points
        self.compute_center()

    def update_normalized_points(self, new_points: list[Point]):
        self._normalized_points = new_points
        self.compute_normalized_center()

    def get_descriptor(self) -> ObjectDescriptor:
        descriptor = ObjectDescriptor(self._name)
        descriptor.vertices = [(p.x, p.y, 0.0) for p in self._points]
        descriptor.color = self._color
        descriptor.id = self.id
        return descriptor

    @staticmethod
    def get_2d_object(descriptor: ObjectDescriptor):
        points = ObjectDescriptor.vertices_to_points(descriptor.vertices)
        match len(points):
            case 0:
                return None
            case 1:
                return PointObject(descriptor.name, points, descriptor.color)
            case 2:
                return LineSegmentObject(descriptor.name, points, descriptor.color)
            case _:
                return WireframeObject(
                    descriptor.name,
                    points,
                    descriptor.color,
                    ObjectType.POLYGON,
                    descriptor.points,
                    descriptor.lines,
                    descriptor.faces,
                )


class PointObject(GraphicObject):
    def __init__(self, name: str, points: list, color) -> None:
        super().__init__(name, points, color)
        self._type = ObjectType.POINT

    def draw(
            self,
            context: cairo.Context,
            viewport_transform: "function",
            window_min: Point,
            window_max: Point,
            clipping: Clipping
    ):
        if clipping.clip_point(window_max, window_min, self._normalized_points[0]):
            new_point = viewport_transform(self._normalized_points[0])
            second_point = Point(new_point.x + 1, new_point.y + 1)
            super().draw_line(context, new_point, second_point)

    def get_descriptor(self) -> ObjectDescriptor:
        descriptor = super().get_descriptor()
        descriptor.points = [-1]
        return descriptor


class LineSegmentObject(GraphicObject):
    def __init__(self, name: str, points: list, color) -> None:
        super().__init__(name, points, color)
        self._type = ObjectType.LINE

    def draw(
            self,
            context: cairo.Context,
            viewport_transform: "function",
            window_min: Point,
            window_max: Point,
            clipping: Clipping
    ):
        new_line = clipping.clip_line(
            window_max,
            window_min,
            self._normalized_points[0],
            self._normalized_points[1],
        )
        if new_line:
            initial_point = viewport_transform(new_line[0])
            end_point = viewport_transform(new_line[1])
            super().draw_line(context, initial_point, end_point)

    def get_descriptor(self) -> ObjectDescriptor:
        descriptor = super().get_descriptor()
        descriptor.lines = [(-2, -1)]
        return descriptor


class WireframeObject(GraphicObject):
    _point_indexes: List[int]
    _lines_indexes: List[List[int]]
    _faces_indexes: List[List[int]]

    def __init__(
            self,
            name: str,
            points: list,
            color,
            wtype=ObjectType.POLYGON,
            point_indexes=None,
            lines_indexes=None,
            faces_indexes=None,
    ) -> None:
        super().__init__(name, points, color)
        self._type = wtype
        self._point_indexes = point_indexes if point_indexes is not None else []
        self._lines_indexes = lines_indexes if lines_indexes is not None else []
        self._faces_indexes = faces_indexes if faces_indexes is not None else []

    def draw(
            self,
            context: cairo.Context,
            viewport_transform: Callable[[Point], Point],
            window_min: Point,
            window_max: Point,
            clipping: Clipping
    ):

        for i in self._point_indexes:
            self._draw_point(context, i, viewport_transform, window_min, window_max, clipping)

        for line in self._lines_indexes:
            self._draw_line(context, line, viewport_transform, window_min, window_max, clipping)

        for face in self._faces_indexes:
            self._draw_face(context, face, viewport_transform, window_min, window_max, clipping)

    def get_descriptor(self) -> ObjectDescriptor:
        descriptor = super().get_descriptor()
        len_vertices = len(self._points)
        descriptor.points = [i - len_vertices for i in self._point_indexes]

        new_lines = []
        for line in self._lines_indexes:
            new_lines.append([i - len_vertices for i in line])
        descriptor.lines = new_lines

        new_faces = []
        for face in self._faces_indexes:
            new_faces.append([i - len_vertices for i in face])
        descriptor.faces = new_faces

        return descriptor

    def _draw_point(self, context: cairo.Context, index: int, viewport_transform, window_min: Point,
                    window_max: Point,
                    clipping: Clipping):
        point = self._normalized_points[0]
        if clipping.clip_point(window_max, window_min, point):
            new_point = viewport_transform(point)
            super().draw_line(context, new_point, Point(new_point.x + 1, new_point.y + 1))

    def _draw_line(
            self, context: cairo.Context, line_indexes: List[int], viewport_transform, window_min: Point,
            window_max: Point,
            clipping: Clipping
    ):
        last_index, *others = line_indexes
        for i in others:
            point1 = self.normalized_points[last_index]
            point2 = self.normalized_points[i]
            last_index = i

            new_line = clipping.clip_line(window_max, window_min, point1, point2)
            if new_line:
                initial_point = viewport_transform(new_line[0])
                end_point = viewport_transform(new_line[1])
                super().draw_line(context, initial_point, end_point)

    def _draw_face(
            self, context: cairo.Context, face_indexes: List[int], viewport_transform, window_min: Point,
            window_max: Point,
            clipping: Clipping
    ):
        context.set_source_rgb(*self._color)

        # Devo adquirir os pontos na ordem correta!
        normalized_face = [self.normalized_points[i] for i in face_indexes]

        # Pegar linhas clipadas com um método de clipping e desenhar as linhas...
        new_lines = clipping.clip_polygon(normalized_face, window_max, window_min)

        # print(new_lines)

        print(new_lines[0][0])
        point1 = viewport_transform(new_lines[0][0])

        context.move_to(point1.x, point1.y)

        for line in new_lines:
            point2 = viewport_transform(line[1])
            context.line_to(point2.x, point2.y)

        context.close_path()
        context.fill()
