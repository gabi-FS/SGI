from typing import Any, Dict
import cairo

from globals import ObjectType, TransformationType
from system.basics import Point
from system.files import ObjectDescriptor
from system.objects import (
    GraphicObject,
    LineSegmentObject,
    PointObject,
    WireframeObject,
)
from system.transform import Transformation
from system.clipping import Clipping
import numpy as np


class Window(GraphicObject):
    _points: list[Point]  # no caso da Window, só tem 2 pontos da diagonal:
    #                       o canto inferior esquerdo e o canto superior direito

    _name: str
    _center: Point
    _type: ObjectType
    _color: tuple
    _normalized_points: list[Point]
    _normalized_center: Point
    _scale_x: float
    _scale_y: float

    def __init__(self, initial_coord: Point, size: tuple[int, int]) -> None:
        self._name = "Window"
        self._color = (1, 0.886, 0)
        self._type = ObjectType.WIREFRAME_POLYGON
        self._points = [initial_coord]
        self._points.append(Point(initial_coord.x, initial_coord.y + size[1]))
        self._points.append(Point(initial_coord.x + size[0], initial_coord.y + size[1]))
        self._points.append(Point(initial_coord.x + size[0], initial_coord.y))
        # coordenadas da window vão ser sempre [(Xmin, Ymin), (Xmin, Ymax), (Xmax, Ymax), (Xmax, Ymin),]
        self._normalized_points = [
            Point(-1, -1),
            Point(-1, 1),
            Point(1, 1),
            Point(1, -1),
        ]
        self._normalized_center = Point(0, 0)
        self._scale_x = 2 / size[0]
        self._scale_y = 2 / size[1]
        self.compute_center()

    @property
    def scale_x(self):
        return self._scale_x

    @property
    def scale_y(self):
        return self._scale_y

    def draw(
        self,
        context: cairo.Context,
        viewport_transform,
        window_min: Point = None,
        window_max: Point = None,
    ):

        first_point, *others = self._normalized_points
        new_first_point = viewport_transform(first_point)

        for point in others:
            end_point = viewport_transform(point)

            super().draw_line(context, new_first_point, end_point)
            new_first_point = end_point

        new_end_point = viewport_transform(self._normalized_points[0])

        super().draw_line(context, new_first_point, new_end_point)

    def scaling(self, factor: float):
        """
        Scales the window using the given factor.

        Args:
            factor: scaling factor for scaling the window:
                0 < factor < 1  : zoom in
                factor > 1      : zoom out
        """
        matrix = Transformation.get_scaling_about_point(self._center, factor, factor)
        self._points = Transformation.transform_points(self._points, matrix)
        self._scale_x *= factor
        self._scale_y *= factor
        self.compute_center()

    def zoom_in(self, amount: float = 0.05):
        self.scaling(1.0 + amount)

    def zoom_out(self, amount: float = 0.05):
        self.scaling(1.0 - amount)

    def translate(self, transform: Transformation, x, y):
        """
        Translates the window by a specified x and y distance.

        Args:
            transform: transformation class
            x: translating factor in x-axis
            y: translating factor in y-axis
        """
        angle = self.get_rotation_angle()
        matrix = transform.get_rotation_about_point(self._center, angle)
        matrix = matrix @ transform.get_translation_matrix(x, y)
        matrix = matrix @ transform.get_rotation_about_point(self._center, -angle)
        self._points = transform.transform_points(self._points, matrix)
        self.compute_center()

    def up(self, transform: Transformation, distance: float = 10):
        self.translate(transform, 0, distance)

    def down(self, transform: Transformation, distance: int = 10):
        self.translate(transform, 0, -distance)

    def left(self, transform: Transformation, distance: float = 10):
        self.translate(transform, -distance, 0)

    def right(self, transform: Transformation, distance: int = 10):
        self.translate(transform, distance, 0)

    def rotation(self, angle: float):
        matrix = Transformation.get_rotation_about_point(self._center, angle)
        self._points = Transformation.transform_points(self._points, matrix)
        self.compute_center()

    def get_up_vector(self) -> Point:
        return self._points[2] - self._points[3]

    def get_rotation_angle(self) -> float:
        up_v = self.get_up_vector()
        angulo = Point.angle_between_vectors(Point(0, 1), up_v)
        angulo = np.rad2deg(angulo)
        return angulo


class ViewPort:
    _size: tuple[int, int]
    _window: Window  # viewport precisa ter acesso à window
    _clipping_area: int

    def __init__(
        self, size: tuple[int, int] = None, window: Window = None, area: int = 0.05
    ) -> None:
        if size and window:
            self._size = size
            self._window = window
            self._clipping_area = area

    @property
    def window(self):
        return self._window

    def transform(self, point: Point) -> Point:
        w_points = self._window.normalized_points
        max_w = w_points[2] + Point(self._clipping_area, self._clipping_area)
        min_w = w_points[0] - Point(self._clipping_area, self._clipping_area)

        vp_x = (point.x - min_w.x) / (max_w.x - min_w.x) * (self._size[0])
        vp_y = (1 - ((point.y - min_w.y) / (max_w.y - min_w.y))) * (self._size[1])
        return Point(vp_x, vp_y)


class DisplayFile:
    _objects: Dict[int, GraphicObject]
    _view_port: ViewPort
    _transformation: Transformation

    def __init__(self, view_port: ViewPort, transformation: Transformation) -> None:
        self._view_port = view_port
        self._transformation = transformation
        self._objects = {}
        self.update_normalization()

    @property
    def transformation(self) -> Transformation:
        return self._transformation

    def create_object(self, object_type, name, input_data, color) -> int:
        new_input = [Point(*x) for x in input_data]
        match object_type:
            case ObjectType.POINT:
                obj = PointObject(name, new_input, color)
            case ObjectType.LINE:
                obj = LineSegmentObject(name, new_input, color)
            case ObjectType.WIREFRAME_POLYGON:
                obj = WireframeObject(name, new_input, color)
            case ObjectType.FILLED_POLYGON:
                n_points = len(new_input)
                obj = WireframeObject(
                    name, new_input, color, faces_indexes=[list(range(n_points))]
                )
        self.add_object(obj)
        self.normalize_object(obj)
        return obj.id

    def add_object(self, obj: GraphicObject):
        self.normalize_object(obj)
        self._objects[obj.id] = obj

    def normalize_object(self, obj: GraphicObject):
        new_points = self._transformation.transform_points(
            obj.points, self._transformation.normalizing_matrix
        )
        obj.update_normalized_points(new_points)

    def transform_object(
        self, object_id: int, object_input: Dict[TransformationType, Any]
    ):
        graphic_object = self.get_object(object_id)
        new_points = self.transformation.get_transformed_points(
            graphic_object,
            object_input,
            window_angle=self._view_port.window.get_rotation_angle(),
            window_center=self._view_port.window.center,
        )
        graphic_object.update_points(new_points)
        self.normalize_object(graphic_object)

    def on_draw(self, context: cairo.Context):
        self._view_port.window.draw(context, self._view_port.transform)
        for obj in self._objects.values():
            obj.draw(
                context,
                self._view_port.transform,
                self._view_port.window.normalized_points[0],
                self._view_port.window.normalized_points[2],
            )

    def get_object(self, object_id: int) -> GraphicObject:
        return self._objects.get(object_id)

    def get_object_descriptors(self) -> list[ObjectDescriptor]:
        return [obj.get_descriptor() for obj in self._objects.values()]

    def update_normalization(self):
        window = self._view_port.window
        self._transformation.set_normalizing_matrix(
            window.center, window.get_up_vector(), window.scale_x, window.scale_y
        )
        for obj in self._objects.values():
            self.normalize_object(obj)

    def on_zoom_in(self):
        self._view_port.window.zoom_in()
        self.update_normalization()

    def on_zoom_out(self):
        self._view_port.window.zoom_out()
        self.update_normalization()

    def on_up(self):
        self._view_port.window.up(self._transformation)
        self.update_normalization()

    def on_left(self):
        self._view_port.window.left(self._transformation)
        self.update_normalization()

    def on_right(self):
        self._view_port.window.right(self._transformation)
        self.update_normalization()

    def on_down(self):
        self._view_port.window.down(self._transformation)
        self.update_normalization()

    def on_rotate(self, angle: float):
        """
        Args:
            angle: window rotation angle in degrees
        """
        self._view_port.window.rotation(angle)
        self.update_normalization()
