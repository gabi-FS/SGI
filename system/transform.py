import numpy as np
from basics import Point


class Transformation:

    def __init__(self) -> None:
        pass

    @staticmethod
    def transform(points: list[Point], matrix: np.matrix) -> list[Point]:
        result = []
        for p in points:
            coord = matrix * np.matrix(p.get_homogeneous_matrix())
            new_point = Point(coord[0], coord[1])
            result.append(new_point)
