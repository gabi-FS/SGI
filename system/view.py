from typing import Any, Dict

import cairo
import numpy as np
from cupshelpers.ppds import normalize

from globals import LineClippingType, ObjectType, TransformationType
from system.basics import Point
from system.clipping import Clipping
from system.files import ObjectDescriptor
from system.objects import (
    GraphicObject,
    LineSegmentObject,
    PointObject,
    WireframeObject,
    BezierCurve,
    BSplineCurve,
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
    _rotation_matrix: np.array
    _scale_x: float
    _scale_y: float

    def __init__(self, initial_coord: Point, size: tuple[int, int]) -> None:
        color = (1, 0.886, 0)
        points = [initial_coord]
        points.append(Point(initial_coord.x, initial_coord.y + size[1]))
        points.append(Point(initial_coord.x + size[0], initial_coord.y + size[1]))
        points.append(Point(initial_coord.x + size[0], initial_coord.y))
        # coordenadas da window vão ser sempre [(Xmin, Ymin), (Xmin, Ymax), (Xmax, Ymax), (Xmax, Ymin),]
        super().__init__("Window", points, color)
        self._type = ObjectType.WIREFRAME_POLYGON
        self._normalized_points = [
            Point(-1, -1),
            Point(-1, 1),
            Point(1, 1),
            Point(1, -1),
        ]
        self._normalized_center = Point(0, 0)
        self._scale_x = 2 / size[0]
        self._scale_y = 2 / size[1]

    @property
    def scale_x(self):
        return self._scale_x

    @property
    def scale_y(self):
        return self._scale_y

    @property
    def rotation_matrix(self):
        return self._rotation_matrix

    @property
    def inverse_rotation_matrix(self):
        return np.linalg.inv(self._rotation_matrix)

    def draw(
            self,
            context: cairo.Context,
            viewport_transform,
            window_min: Point = None,
            window_max: Point = None,
            clipping=None,
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
        matrix = Transformation.get_scaling_about_point(self._center, factor, factor, 1)
        self._points = Transformation.transform_points(self._points, matrix)
        self._scale_x *= factor
        self._scale_y *= factor
        self.compute_center()

    def zoom_in(self, amount: float = 0.05):
        self.scaling(1.0 + amount)

    def zoom_out(self, amount: float = 0.05):
        self.scaling(1.0 - amount)

    def translate(self, transform: Transformation, x, y, z=0):
        """
        Translates the window by a specified x and y distance.

        Args:
            transform: transformation class
            x: translating factor in x-axis
            y: translating factor in y-axis
        """

        translate_back_from_origin = transform.get_translation_matrix(
            self._center.x, self._center.y, self._center.z
        )
        rotate_again = self._rotation_matrix
        translate_amount = transform.get_translation_matrix(x, y, z)
        undo_rotation = self.inverse_rotation_matrix
        translate_back_to_origin = transform.get_translation_matrix(
            -self._center.x, -self._center.y, -self._center.z
        )

        matrix = (
                translate_back_from_origin
                @ undo_rotation
                @ translate_amount
                @ rotate_again
                @ translate_back_to_origin
        )

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

    def front(self, transform: Transformation, distance: int = 10):
        self.translate(transform, 0, 0, distance)

    def back(self, transform: Transformation, distance: int = 10):
        self.translate(transform, 0, 0, -distance)

    def rotation(self, x_angle: float, y_angle: float, z_angle: float):
        translation_back = Transformation.get_translation_matrix(
            self._center.x, self._center.y, self._center.z
        )

        x_rad = np.deg2rad(x_angle)
        y_rad = np.deg2rad(y_angle)
        z_rad = np.deg2rad(z_angle)

        rotation = Transformation.get_rotation_matrix(x_rad, y_rad, z_rad)
        translation = Transformation.get_translation_matrix(
            -self._center.x, -self._center.y, -self._center.z
        )

        matrix = translation_back @ rotation @ translation
        self._points = Transformation.transform_points(self._points, matrix)
        self.compute_center()
        self._rotation_matrix = rotation @ self._rotation_matrix

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
    _clipping_type: LineClippingType

    def __init__(
            self, size: tuple[int, int] = None, window: Window = None, area: float = 0.10
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
    _clipping: Clipping

    def __init__(self, view_port: ViewPort, transformation: Transformation) -> None:
        self._view_port = view_port
        self._transformation = transformation
        self._objects = {}
        self._clipping = Clipping(LineClippingType.LIANG_BARSKY)
        self.update_normalization()

    @property
    def transformation(self) -> Transformation:
        return self._transformation

    def change_clipping_type(self, new_type: LineClippingType):
        self._clipping.line_type = new_type

    def create_object(self, object_type, name, input_data, color) -> int:
        new_input = [Point(*x) for x in input_data]
        n_points = len(new_input)
        match object_type:
            case ObjectType.POINT:
                obj = PointObject(name, new_input, color)
            case ObjectType.LINE:
                obj = LineSegmentObject(name, new_input, color)
            case ObjectType.WIREFRAME_POLYGON:
                obj = WireframeObject(
                    name,
                    new_input,
                    color,
                    ObjectType.WIREFRAME_POLYGON,
                    lines_indexes=[list(range(n_points)) + [0]],
                )
            case ObjectType.FILLED_POLYGON:
                obj = WireframeObject(
                    name,
                    new_input,
                    color,
                    ObjectType.FILLED_POLYGON,
                    faces_indexes=[list(range(n_points))],
                )
            case ObjectType.BEZIER_CURVE:
                obj = BezierCurve(name, new_input, color)
            case ObjectType.BSPLINE_CURVE:
                obj = BSplineCurve(name, new_input, color)
        self.add_object(obj)
        self.normalize_object(obj)
        return obj.id

    def add_object(self, obj: GraphicObject):
        self.normalize_object(obj)
        self._objects[obj.id] = obj

    def normalize_object(self, obj: GraphicObject):
        def size(point1: Point, point2: Point) -> float:
            """Size of 3D vector between two points."""
            return ((point1.x - point2.x) ** 2 +
                    (point1.y - point2.y) ** 2 +
                    (point1.z - point2.z) ** 2) ** 0.5

        # Obtenha a janela e o centro
        window = self._view_port.window

        # Defina o tamanho da janela
        window_size = size(window.points[0], window.points[3])
        # # Obtenha a janela e o centro
        COP_DISTANCE = 1  # Usado na projeção

        # Matriz de transformação inicial
        x, y, z = window.center
        to_origin = Transformation.get_translation_matrix(-x, -y, -z)
        rotate = window.inverse_rotation_matrix
        cop_to_origin = Transformation.get_translation_matrix(0, 0, COP_DISTANCE * (window_size / 2))
        scale = Transformation.get_scaling_matrix(window.scale_x, window.scale_y, window.scale_x)

        # Aplicando inversamente
        matrix = scale @ cop_to_origin @ rotate @ to_origin

        # Projeção em perspectiva para cada ponto transformado
        def project(point):
            # Evita divisão por zero, caso z seja zero
            if point.z == 0:
                return Point(point.x, point.y, point.z)
            return Point(point.x * COP_DISTANCE / point.z, point.y * COP_DISTANCE / point.z)

        new_points = Transformation.transform_points(obj.points, matrix)

        obj.update_normalized_points([project(p) for p in new_points])

    def transform_object(
            self, object_id: int, object_input: Dict[TransformationType, Any]
    ):
        graphic_object = self.get_object(object_id)
        new_points = self.transformation.get_transformed_points(
            graphic_object,
            object_input,
            window_rotation=self._view_port.window.rotation_matrix,
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
                self._clipping,
            )

    def get_object(self, object_id: int) -> GraphicObject:
        return self._objects.get(object_id)

    def get_object_descriptors(self) -> list[ObjectDescriptor]:
        return [obj.get_descriptor() for obj in self._objects.values()]

    def update_normalization(self):
        window = self._view_port.window
        self._transformation.set_normalizing_matrix(
            window.center,
            window.rotation_matrix,
            window.scale_x,
            window.scale_y,
            1,
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

    def on_front(self):
        self._view_port.window.front(self._transformation)
        self.update_normalization()

    def on_back(self):
        self._view_port.window.back(self._transformation)
        self.update_normalization()

    def on_rotate(
            self,
            angle_x: float,
            angle_y: float,
            angle_z: float,
    ):
        """
        Args:
            angle: window rotation angle in degrees
        """
        self._view_port.window.rotation(angle_x, angle_y, angle_z)
        self.update_normalization()
