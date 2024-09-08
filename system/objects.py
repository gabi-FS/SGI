from abc import ABC, abstractmethod

from system.basics import Point
from globals import ObjectType


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

    # @abstractmethod
    # def get_center(self):
    #     pass

    @abstractmethod
    def draw(self, context, viewport_transform):
        raise NotImplementedError


class PointObject(GraphicObject):
    def __init__(self, name: str, points: list, color) -> None:
        super().__init__(name, points, color)
        self._type = ObjectType.POINT

    def draw(self, context, viewport_transform):
        # chamar a transformada de viewport
        new_point = viewport_transform(self._points[0])

        context.set_source_rgb(*self._color)
        context.set_line_width(2)
        context.move_to(new_point.x, new_point.y)  # Ponto inicial da linha
        # Ponto final da linha
        context.line_to(new_point.x + 1, new_point.y + 1)
        context.stroke()  # Desenha a linha


class LineSegmentObject(GraphicObject):
    def __init__(self, name: str, points: list, color) -> None:
        super().__init__(name, points, color)
        self._type = ObjectType.LINE

    def draw(self, context, viewport_transform):
        # chamar a transformada de viewport
        initial_point = viewport_transform(self._points[0])
        end_point = viewport_transform(self._points[1])

        context.set_source_rgb(*self._color)
        context.set_line_width(2)
        context.move_to(*initial_point)  # Ponto inicial da linha
        context.line_to(*end_point)  # Ponto final da linha
        context.stroke()  # Desenha a linha


class WireframeObject(GraphicObject):

    def __init__(self, name: str, points: list, color) -> None:
        super().__init__(name, points, color)
        self._type = ObjectType.POLYGON

    def draw(self, context, viewport_transform):
        first_point, *others = self._points

        # chamar a transformada de viewport
        new_first_point = viewport_transform(first_point)

        for point in others:
            end_point = viewport_transform(point)

            context.set_source_rgb(*self._color)
            context.set_line_width(2)
            context.move_to(*new_first_point)  # Ponto inicial da linha
            context.line_to(*end_point)  # Ponto final da linha
            context.stroke()  # Desenha a linha

            new_first_point = end_point

        new_end_point = viewport_transform(self._points[0])
        context.set_source_rgb(*self._color)
        context.set_line_width(2)
        context.move_to(*new_first_point)  # Ponto inicial da linha
        context.line_to(*new_end_point)  # Ponto final da linha
        context.stroke()  # Desenha a linha
