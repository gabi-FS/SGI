import numpy as np


class Point:
    _x: float
    _y: float

    def __init__(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __iter__(self):
        return iter([self._x, self._y])

    def __str__(self) -> str:
        return f"Point: x={self._x}, y={self._y}"

    def get_homogeneous_matrix(self) -> np.array:
        return np.array([[self._x], [self._y], [1.0]])

    def get_array(self) -> np.array:
        return np.array([self._x, self._y])

    def norm(self) -> float:
        array = self.get_array()
        return np.linalg.norm(array)

    @classmethod
    def inner_product(cls, vector1: "Point", vector2: "Point"):
        """
        Produto interno de 2 vetores
        """
        return (vector1.x * vector2.x) + (vector1.y * vector2.y)

    @classmethod
    def angle_between_vectors(cls, vector1: "Point", vector2: "Point"):
        """
        Retorna o ângulo entre 2 vetores
        """
        a = cls.inner_product(vector1, vector2)
        b = vector1.norm() * vector2.norm()
        return np.arccos(a / b)

    @classmethod
    def get_geometric_center(cls, points: list["Point"]) -> "Point":
        x_list = []
        y_list = []
        for p in points:
            x_list.append(p.x)
            y_list.append(p.y)

        center_x = np.mean(x_list)
        center_y = np.mean(y_list)

        center = Point(center_x, center_y)

        return center
