from typing import Any, Dict

import numpy as np

from globals import RotationType, TransformationType
from system.basics import Point
from system.objects import GraphicObject
from utils import get_tuple_from_object, get_tuple_from_str


class Transformation:

    _normalizing_matrix: np.array

    def __init__(self) -> None:
        self._normalizing_matrix = np.identity(3)

    @property
    def normalizing_matrix(self):
        return self._normalizing_matrix

    @staticmethod
    def get_transformed_points(
        graphic_object: GraphicObject, transform_input: Dict[TransformationType, Any]
    ) -> list[Point]:
        """
        Dada a entrada e os dados do objeto, retorna novos pontos com as transformações aplicadas.
        """
        identity_matrix = np.identity(3)
        transforming_matrix = identity_matrix

        transforming_matrix = Transformation.apply_translation(
            transforming_matrix, transform_input[TransformationType.TRANSLATION]
        )
        transforming_matrix = Transformation.apply_scale(
            transforming_matrix,
            transform_input[TransformationType.SCALING],
            graphic_object.center,
        )
        transforming_matrix = Transformation.apply_rotation(
            transforming_matrix,
            transform_input[TransformationType.ROTATION],
            graphic_object.center,
        )

        if np.array_equal(transforming_matrix, identity_matrix):
            return graphic_object.points
        else:
            return Transformation.transform_points(
                graphic_object.points, transforming_matrix
            )

    @staticmethod
    def apply_translation(
        curr_matrix: np.array, data_input: Dict[str, str]
    ) -> np.array:
        """
        Method to apply translation matrix.
        It multiplies the current matrix by the translation from data input.

        Args:
            curr_matrix: current matrix (numpy array)
            data_input: dictionary with translation data

        Returns:
            resulting matrix (numpy array) applying translation
        """
        try:
            x, y = get_tuple_from_object(data_input, 0)
        except ValueError:
            return curr_matrix
        return curr_matrix @ Transformation.get_translation_matrix(x, y)

    @staticmethod
    def apply_scale(
        curr_matrix, data_input: Dict[str, str], object_center: Point
    ) -> np.array:
        """
        Method to apply scaling matrix.
        It multiplies the current matrix by the scaling from data input and object center (anchor).

        Args:
            curr_matrix: current matrix (numpy array)
            data_input: dictionary with scaling data
            object_center: center for anchoring scaling

        Returns:
            resulting matrix (numpy array) applying scaling
        """
        try:
            x, y = get_tuple_from_object(data_input, 1)
        except ValueError:
            return curr_matrix
        return curr_matrix @ Transformation.get_scaling_about_point(object_center, x, y)

    @staticmethod
    def apply_rotation(
        curr_matrix: np.array, data_input: Dict[str, str], object_center: Point
    ) -> np.array:
        """
        Method to apply rotation matrix. It multiplies the current matrix by the rotation from data input and object.

        Args:
            curr_matrix: current matrix (numpy array)
            data_input: dictionary with rotation data
            object_center: center for anchoring scaling (if necessary)

        Returns:
            resulting matrix (numpy array) applying rotation
        """
        angle = data_input["angle"].strip()
        if angle == "":
            return curr_matrix
        rotation_type, angle = data_input["type"], float(angle)
        match rotation_type:
            case RotationType.WORLD_CENTER:
                rotation_matrix = Transformation.get_rotation_matrix(angle)
            case RotationType.OBJECT_CENTER:
                rotation_matrix = Transformation.get_rotation_about_point(
                    object_center, angle
                )
            case RotationType.AROUND_POINT:
                numbers = get_tuple_from_str(data_input["point"])
                rotation_matrix = Transformation.get_rotation_about_point(
                    Point(*numbers), angle
                )
        return curr_matrix @ rotation_matrix

    @staticmethod
    def transform_points(points: list[Point], matrix: np.array) -> list[Point]:
        result = []
        for point in points:
            coord = matrix @ np.array(point.get_homogeneous_matrix())
            new_point = Point(coord[0, 0], coord[1, 0])
            result.append(new_point)
        return result

    @staticmethod
    def get_rotation_about_point(point: Point, angle: float) -> np.array:
        """
        Method to build a rotation matrix about a point.

        Args:
            point: point of reference to the rotation
            angle: rotation angle in degrees

        Returns:
            rotation matrix (numpy array)
        """
        x, y = point.x, point.y
        trans_to_point = Transformation.get_translation_matrix(x, y)
        rotation = Transformation.get_rotation_matrix(angle)
        trans_back = Transformation.get_translation_matrix(-x, -y)
        return trans_to_point @ rotation @ trans_back

    @staticmethod
    def get_scaling_about_point(
        point: Point, x_factor: float, y_factor: float
    ) -> np.array:
        """
        Method to build a scaling matrix about a point.

        Args:
            point: point of reference to the scaling
            x_factor: scaling factor in the x direction
            y_factor: scaling factor in the y direction

        Returns:
            scaling matrix (numpy array)
        """
        x, y = point.x, point.y
        trans_to_point = Transformation.get_translation_matrix(x, y)
        scaling = Transformation.get_scaling_matrix(x_factor, y_factor)
        trans_back = Transformation.get_translation_matrix(-x, -y)
        return trans_to_point @ scaling @ trans_back

    @staticmethod
    def get_scaling_matrix(x_factor: float, y_factor: float) -> np.array:
        """
        Method to build a scaling matrix.

        Args:
            x_factor: scaling factor in x axis
            y_factor: scaling factor in y axis

        Returns:
            scaling matrix (numpy array)
        """
        return np.array([[x_factor, 0, 0], [0, y_factor, 0], [0, 0, 1]])

    @staticmethod
    def get_translation_matrix(x_factor: float, y_factor: float) -> np.array:
        """
        Method to build a translation matrix.

        Args:
            x_factor: translation factor in x axis
            y_factor: translation factor in y axis

        Returns:
            translation matrix (numpy array)
        """
        return np.array([[1, 0, x_factor], [0, 1, y_factor], [0, 0, 1]])

    @staticmethod
    def get_rotation_matrix(angle: float) -> np.array:
        """
        Method to build a rotation matrix.

        Args:
            angle: rotation angle in degrees

        Returns:
            rotation matrix (numpy array)
        """
        angle_rad = np.deg2rad([angle])
        cos = np.cos(angle_rad)[0]
        sin = np.sin(angle_rad)[0]
        return np.array([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]])

    def set_normalizing_matrix(
        self,
        window_center: Point,
        up_vector: Point,
        scale: float,
    ) -> np.array:
        matrix = self.get_translation_matrix(-window_center.x, -window_center.y)
        angulo = Point.angle_between_vectors(Point(0, 1), up_vector)
        angulo = np.rad2deg(angulo)
        matrix = matrix @ self.get_rotation_about_point(
            window_center, -angulo
        )  ## talvez esteja em rad e tenha que mudar pra deg
        matrix = matrix @ self.get_scaling_about_point(window_center, scale, scale)
        self._normalizing_matrix = matrix
        print("Normalizing")
        print(up_vector)
        print(scale)

        return matrix
