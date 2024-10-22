from abc import ABC, abstractmethod
from typing import Callable, List

import cairo

from globals import ObjectType
from system.basics import Point
from system.clipping import Clipping
from system.files import ObjectDescriptor
import numpy as np


class GraphicObject(ABC):
    _id_increment = 0

    _id = int
    _name: str
    _points: list[Point]  # lista de pontos (conjuntos de coordenadas x e y)
    _center: Point
    _type: ObjectType
    _color: tuple
    _normalized_points: list[Point]
    _normalized_center: Point
    _rotation_matrix: np.array

    def __init__(self, name: str, points: list, color) -> None:
        self._id = GraphicObject._id_increment
        GraphicObject._id_increment += 1
        self._name = name
        self._points = points
        self._color = color
        self._normalized_points = points
        self._normalized_center = self.compute_center()
        self._rotation_matrix = np.identity(4)

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
        clipping: Clipping,
    ):
        raise NotImplementedError

    def draw_line(self, context: cairo.Context, point1: Point, point2: Point):
        # print(self._normalized_points[0])
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
        clipping: Clipping,
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
        clipping: Clipping,
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
        clipping: Clipping,
    ):

        for i in self._point_indexes:
            self._draw_point(
                context, i, viewport_transform, window_min, window_max, clipping
            )

        for line in self._lines_indexes:
            self._draw_line(
                context, line, viewport_transform, window_min, window_max, clipping
            )

        for face in self._faces_indexes:
            self._draw_face(
                context, face, viewport_transform, window_min, window_max, clipping
            )

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

    def _draw_point(
        self,
        context: cairo.Context,
        index: int,
        viewport_transform,
        window_min: Point,
        window_max: Point,
        clipping: Clipping,
    ):

        point = self._normalized_points[index]
        if clipping.clip_point(window_max, window_min, point):
            new_point = viewport_transform(point)
            super().draw_line(
                context, new_point, Point(new_point.x + 1, new_point.y + 1)
            )

    def _draw_line(
        self,
        context: cairo.Context,
        line_indexes: List[int],
        viewport_transform,
        window_min: Point,
        window_max: Point,
        clipping: Clipping,
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
        self,
        context: cairo.Context,
        face_indexes: List[int],
        viewport_transform,
        window_min: Point,
        window_max: Point,
        clipping: Clipping,
    ):
        context.set_source_rgb(*self._color)
        normalized_face = [self.normalized_points[i] for i in face_indexes]
        new_lines = clipping.clip_polygon(normalized_face, window_max, window_min)

        if new_lines:
            point1 = viewport_transform(new_lines[0][0])
            context.move_to(point1.x, point1.y)

            for line in new_lines:
                point2 = viewport_transform(line[1])
                context.line_to(point2.x, point2.y)

            context.close_path()
            context.fill()


class Curve(GraphicObject):
    _drawing_step: int

    @abstractmethod
    def compute_curve_points(self, control_points: List[Point]) -> List[Point]:
        raise NotImplementedError

    def draw(
        self,
        context: cairo.Context,
        viewport_transform: Callable[[Point], Point],
        window_min: Point,
        window_max: Point,
        clipping: Clipping,
    ):
        last_point, *others = self.normalized_points
        for next_point in others:
            new_line = clipping.clip_line(
                window_max, window_min, last_point, next_point
            )
            if new_line:
                initial_point = viewport_transform(new_line[0])
                end_point = viewport_transform(new_line[1])
                super().draw_line(context, initial_point, end_point)
            last_point = next_point

    def get_descriptor(self) -> ObjectDescriptor:
        descriptor = super().get_descriptor()
        len_vertices = len(self._points)
        descriptor.lines = [[i - len_vertices for i in range(len_vertices)]]
        return descriptor


class BezierCurve(Curve):

    def __init__(self, name: str, points: List[Point], color, drawing_step=30) -> None:
        self._drawing_step = drawing_step
        n_control_points = len(points)
        real_points = []
        for i in range(0, n_control_points - 3, 3):
            # Cria curvas a cada 4 pontos para garantir continuidade G(0):
            p = self.compute_curve_points(points[i : i + 4])
            real_points.extend(p)  # Concatena os pontos calculados

        super().__init__(name, real_points, color)

    def compute_curve_points(self, control_points: List[Point]) -> List[Point]:
        # Matriz da curva de Bézier cúbica
        m = np.array([[1, 0, 0, 0], [-3, 3, 0, 0], [3, -6, 3, 0], [-1, 3, -3, 1]])
        computed_points = []

        for val in range(self._drawing_step + 1):  # `val` vai de 0 a drawing_step
            t = val / self._drawing_step  # Corrigir t para variar entre 0 e 1

            # Vetor [1, t, t^2, t^3]
            t_matrix = np.array([1, t, t * t, t * t * t])
            t_m_matrix = t_matrix @ m  # Multiplica t pela matriz da curva

            # Calcula as coordenadas x e y
            x_value = t_m_matrix @ np.array(
                [
                    [control_points[0].x],
                    [control_points[1].x],
                    [control_points[2].x],
                    [control_points[3].x],
                ]
            )
            y_value = t_m_matrix @ np.array(
                [
                    [control_points[0].y],
                    [control_points[1].y],
                    [control_points[2].y],
                    [control_points[3].y],
                ]
            )

            computed_points.append(Point(x_value[0], y_value[0]))

        return computed_points


class BSplineCurve(Curve):

    def __init__(self, name: str, points: List[Point], color, drawing_step=15) -> None:
        self._drawing_step = drawing_step
        n_control_points = len(points)

        # Calcula segmentos da B-Spline utilizando blocos de 4 pontos consecutivos
        real_points = []
        for i in range(n_control_points - 3):
            p = self.compute_curve_points(points[i : i + 4])
            real_points.extend(p)

        super().__init__(name, real_points, color)

    def compute_curve_points(self, control_points: List[Point]) -> List[Point]:
        computed_points = []

        # Matriz da B-Spline cúbica usando np.array
        b_spline_matrix = (1 / 6) * np.array(
            [[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]]
        )

        delta = 1 / self._drawing_step

        # Matriz de diferenças forward
        diff_matrix = np.array(
            [
                [0, 0, 0, 1],
                [delta**3, delta**2, delta, 0],
                [6 * delta**3, 2 * delta**2, 0, 0],
                [6 * delta**3, 0, 0, 0],
            ]
        )

        p1, p2, p3, p4 = control_points

        g_matrix_x = np.array([[p1.x], [p2.x], [p3.x], [p4.x]])
        g_matrix_y = np.array([[p1.y], [p2.y], [p3.y], [p4.y]])

        # Multiplica a matriz de controle pelos coeficientes da B-Spline
        coeff_matrix_x = b_spline_matrix @ g_matrix_x
        coeff_matrix_y = b_spline_matrix @ g_matrix_y

        # Aplica Forward Differences para as coordenadas x e y
        initial_conditions_matrix_x = diff_matrix @ coeff_matrix_x
        initial_conditions_matrix_y = diff_matrix @ coeff_matrix_y

        new_x = initial_conditions_matrix_x[0, 0]
        new_y = initial_conditions_matrix_y[0, 0]

        delta_x = initial_conditions_matrix_x[1, 0]
        delta2_x = initial_conditions_matrix_x[2, 0]
        delta3_x = initial_conditions_matrix_x[3, 0]

        delta_y = initial_conditions_matrix_y[1, 0]
        delta2_y = initial_conditions_matrix_y[2, 0]
        delta3_y = initial_conditions_matrix_y[3, 0]

        # Adiciona o primeiro ponto calculado
        computed_points.append(Point(new_x, new_y))

        # Calcula os próximos pontos incrementando as diferenças
        for _ in range(self._drawing_step):
            new_x += delta_x
            new_y += delta_y

            delta_x += delta2_x
            delta_y += delta2_y

            delta2_x += delta3_x
            delta2_y += delta3_y

            computed_points.append(Point(new_x, new_y))

        return computed_points
