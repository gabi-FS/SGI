import numpy as np
from basics import Point


class Transformation:

    def __init__(self) -> None:
        pass

    @staticmethod
    def transform(points: list[Point], matrix: np.matrix) -> list[Point]:
        result = []
        for p in points:
            print(matrix)
            coord = matrix * np.matrix(p.get_homogeneous_matrix().T)
            print(coord)
            new_point = Point(coord[0].item(0), coord[1].item(0))
            result.append(new_point)
        return result

    @staticmethod
    def get_scaling_matrix(x_factor: float, y_factor: float) -> np.matrix:
        """
        Method to build a scaling matrix.

        Args:
            x_factor: scaling factor in x axis
            y_factor: scaling factor in y axis

        Returns:
            scaling matrix (numpy matrix)
        """
        return np.matrix([[x_factor, 0, 0], [0, y_factor, 0], [0, 0, 1]])

    @staticmethod
    def get_translation_matrix(x_factor: float, y_factor: float) -> np.matrix:
        """
        Method to build a translation matrix.

        Args:
            x_factor: translation factor in x axis
            y_factor: translation factor in y axis

        Returns:
            translation matrix (numpy matrix)
        """
        return np.matrix([[1, 0, x_factor], [0, 1, y_factor], [0, 0, 1]])

    @staticmethod
    def get_rotation_matrix(angle: float) -> np.matrix:
        """
        Method to build a rotation matrix.

        Args:
            angle: rotation angle in radians

        Returns:
            rotation matrix (numpy matrix)
        """
        cos = np.cos([angle])[0]
        sin = np.sin([angle])[0]
        return np.matrix([[-cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])
