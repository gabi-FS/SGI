from globals import ObjectType
from system.basics import Point
from system.objects import (
    GraphicObject,
    LineSegmentObject,
    PointObject,
    WireframeObject,
)


class Window(GraphicObject):
    _points: list[Point]  # no caso da Window, só tem 2 pontos da diagonal:
    #                       o canto inferior esquerdo e o canto superior direito

    _name: str
    _center: tuple[Point]
    _type: ObjectType
    _color: tuple

    def __init__(self, initial_coord: Point, size: tuple[int, int]) -> None:
        self._name = "Window"
        self._type = ObjectType.POLYGON
        self._points = [initial_coord]
        coord_max = Point(initial_coord.x + size[0], initial_coord.y + size[1])
        self._points.append(coord_max)
        # coordenadas da window vão ser sempre [(Xmin, Ymin), (Xmax, Ymax)]

    def draw(self, context, viewport_transform):
        return super().draw(context, viewport_transform)

    def zoom_in(self, distance: int = 10):
        self._points[0] = self._points[0] + Point(distance, distance)
        self._points[1] = self._points[1] - Point(distance, distance)

    def zoom_out(self, distance: int = 10):
        self._points[0] = self._points[0] - Point(distance, distance)
        self._points[1] = self._points[1] + Point(distance, distance)

    def up(self, distance: int = 10):
        self._points[0] = Point(self._points[0].x, self._points[0].y + distance)
        self._points[1] = Point(self._points[1].x, self._points[1].y + distance)

    def left(self, distance: int = 10):
        self._points[0] = Point(self._points[0].x - distance, self._points[0].y)
        self._points[1] = Point(self._points[1].x - distance, self._points[1].y)

    def right(self, distance: int = 10):
        self._points[0] = Point(self._points[0].x + distance, self._points[0].y)
        self._points[1] = Point(self._points[1].x + distance, self._points[1].y)

    def down(self, distance: int = 10):
        self._points[0] = Point(self._points[0].x, self._points[0].y - distance)
        self._points[1] = Point(self._points[1].x, self._points[1].y - distance)


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
            / (w_points[1].x - w_points[0].x)
            * (self._size[0])
        )
        vp_y = (1 - ((point.y - w_points[0].y) / (w_points[1].y - w_points[0].y))) * (
            self._size[1]
        )
        return Point(vp_x, vp_y)


class DisplayFile:
    _objects: list[GraphicObject]
    _view_port: ViewPort

    def __init__(self, view_port: ViewPort) -> None:
        self._view_port = view_port
        self._objects = []

    def create_object(self, object_type, name, input, color):

        new_input = [Point(*x) for x in input]
        match object_type:
            case ObjectType.POINT:
                obj = PointObject(name, new_input, color)
            case ObjectType.LINE:
                obj = LineSegmentObject(name, new_input, color)
            case ObjectType.POLYGON:
                obj = WireframeObject(name, new_input, color)
        self._objects.append(obj)

    def on_draw(self, context):
        for obj in self._objects:
            obj.draw(context, self._view_port.transform)

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
