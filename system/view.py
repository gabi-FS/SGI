from system.basics import Point
from globals import ObjectType
from system.objects import (
    GraphicObject,
    LineSegmentObject,
    PointObject,
    WireframeObject,
)


class Window(GraphicObject):
    _points: list[Point]  # no caso da Window, só tem 2 pontos da diagonal:
    #                       o canto inferior esquerdo e o canto superior direito
    _size: tuple[int, int]
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


class ViewPort:
    _size: tuple[int, int]
    _window: (
        Window  # talvez não seja o ideal, mas a viewport precisa ter acesso à window
    )
    # também dá pra passar como parâmetro

    def __init__(self, size: tuple[int, int] = None, window: Window = None) -> None:
        if size and window:
            self._size = size
            self._window = window

    def transform(self, point: Point):
        w_points = self._window.points
        vp_x = (
            (point.x - w_points[0].x)
            / (w_points[1].x - w_points[0].x)
            * (self._size[0])
        )
        vp_y = (1 - (point.y - w_points[0].y) / (w_points[1].y - w_points[0].y)) * (
            self._size[1]
        )
        return Point(vp_x, vp_y)


class DisplayFile:
    _objects: list[GraphicObject]
    _view_port: ViewPort

    def __init__(self, view_port: ViewPort) -> None:
        self._view_port = view_port
        self._objects = []

    def create_object(self, object_type, name, input):
        print("executou create_object")
        color = (1, 0, 0)  # Default no momento: RED
        # RESOLVER: input não é lista de objetos Point, e sim de (float, float)
        new_input = [Point(*x) for x in input]
        print(object_type)
        print(type(object_type))
        match object_type.value:
            case ObjectType.POINT.value:
                obj = PointObject(name, new_input, color)
            case ObjectType.LINE.value:
                obj = LineSegmentObject(name, new_input, color)
            case ObjectType.POLYGON.value:
                obj = WireframeObject(name, new_input, color)
        self._objects.append(obj)

    def on_draw(self, context):
        print("Tentou desenhar objetos")
        print(self._objects)

        for obj in self._objects:
            obj.draw(context, self._view_port.transform)
