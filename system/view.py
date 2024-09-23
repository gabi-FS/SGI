from typing import Dict

import cairo

from globals import ObjectType
from system.basics import Point
from system.objects import (
    GraphicObject,
    LineSegmentObject,
    PointObject,
    WireframeObject,
)
from system.transform import Transformation


class Window(GraphicObject):
    _points: list[Point]  # no caso da Window, só tem 2 pontos da diagonal:
    #                       o canto inferior esquerdo e o canto superior direito

    _name: str
    _center: Point
    _type: ObjectType
    _color: tuple
    _normalized_points: list[Point]
    _normalized_center: Point

    def __init__(self, initial_coord: Point, size: tuple[int, int]) -> None:
        self._name = "Window"
        self._color = None
        self._type = ObjectType.POLYGON
        self._points = [initial_coord]
        self._points.append(Point(initial_coord.x, initial_coord.y + size[1]))
        self._points.append(Point(initial_coord.x + size[0], initial_coord.y + size[1]))
        self._points.append(Point(initial_coord.x + size[0], initial_coord.y))
        # coordenadas da window vão ser sempre [(Xmin, Ymin), (Xmin, Ymax), (Xmax, Ymin), (Xmin, Ymin),]
        self._normalized_points = [Point(-1, -1), Point(1, 1)]
        self._normalized_center = Point(0, 0)
        print(*self._points)
        self.compute_center()
        print(self._center)

    def draw(self, context: cairo.Context, viewport_transform):
        return super().draw(context, viewport_transform)

    def scale(self, factor: float):
        """
        Scales the window using the given factor.

        Args:
            factor: sacling factor for scaling the window:
                0 < factor < 1  : zoom in
                factor > 1      : zoom out
        """
        matrix = Transformation.get_scaling_about_point(self._center, factor, factor)
        self._points = Transformation.transform_points(self._points, matrix)

    def zoom_in(self, amount: float = 0.05):
        self.scale(1.0 - amount)

    def zoom_out(self, amount: float = 0.05):
        self.scale(1.0 + amount)

    def translate(self, x, y):
        """
        Translates the window by a specified x and y distance.

        Args:
            x: translating factor in x axis
            y: translating factor in y axis
        """
        matrix = Transformation.get_translation_matrix(x, y)
        self._points = Transformation.transform_points(self._points, matrix)

    def up(self, distance: float = 10):
        self.translate(0, distance)

    def down(self, distance: int = 10):
        self.translate(0, -distance)

    def left(self, distance: float = 10):
        self.translate(-distance, 0)

    def right(self, distance: int = 10):
        self.translate(distance, 0)


class ViewPort:
    _size: tuple[int, int]
    _window: Window  # viewport precisa ter acesso à window

    def __init__(self, size: tuple[int, int] = None, window: Window = None) -> None:
        if size and window:
            self._size = size
            self._window = window

    @property
    def window(self):
        return self._window

    def transform(self, point: Point):
        w_points = self._window.points
        vp_x = (
                (point.x - w_points[0].x)
                / (w_points[2].x - w_points[0].x)
                * (self._size[0])
        )
        vp_y = (1 - ((point.y - w_points[0].y) / (w_points[2].y - w_points[0].y))) * (
            self._size[1]
        )
        return Point(vp_x, vp_y)


class DisplayFile:
    _objects: Dict[int, GraphicObject]
    _view_port: ViewPort

    def __init__(self, view_port: ViewPort) -> None:
        self._view_port = view_port
        self._objects = {}

    def create_object(self, object_type, name, input_data, color) -> int:
        new_input = [Point(*x) for x in input_data]
        match object_type:
            case ObjectType.POINT:
                obj = PointObject(name, new_input, color)
            case ObjectType.LINE:
                obj = LineSegmentObject(name, new_input, color)
            case ObjectType.POLYGON:
                obj = WireframeObject(name, new_input, color)
        self.add_object(obj)
        return obj.id

    def add_object(self, obj: GraphicObject):
        self._objects[obj.id] = obj

    def on_draw(self, context: cairo.Context):
        for obj in self._objects.values():
            obj.draw(context, self._view_port.transform)

    def get_object(self, object_id: int) -> GraphicObject:
        return self._objects.get(object_id)

    def on_zoom_in(self):
        self._view_port.window.zoom_in()

    def on_zoom_out(self):
        self._view_port.window.zoom_out()

    def on_up(self):
        self._view_port.window.up()

    def on_left(self):
        self._view_port.window.left()

    def on_right(self):
        self._view_port.window.right()

    def on_down(self):
        self._view_port.window.down()
