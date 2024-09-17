import numpy as np
from system.basics import Point
from globals import TransformationType, RotationType
from system.objects import GraphicObject
from typing import Any, Dict, List, Tuple


class Transformation:

    def __init__(self) -> None:
        pass

    @staticmethod
    def transform_points(points: list[Point], matrix: np.array) -> list[Point]:
        result = []
        for p in points:
            print(matrix)
            coord = matrix @ np.array(p.get_homogeneous_matrix().T)
            print(coord)
            new_point = Point(coord[0, 0], coord[1, 0])
            result.append(new_point)
        return result

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
        x = point.x
        y = point.y
        trans_to_point = Transformation.get_translation_matrix(x, y)
        rot = Transformation.get_rotation_matrix(angle)
        trans_back = Transformation.get_translation_matrix(-x, -y)
        return trans_to_point @ rot @ trans_back

    @staticmethod
    def get_scaling_about_point(
        point: Point, x_factor: float, y_factor: float
    ) -> np.array:
        """
        Method to build a rotation matrix about a point.

        Args:
            point: point of reference to the rotation
            angle: rotation angle in degrees

        Returns:
            rotation matrix (numpy array)
        """
        x = point.x
        y = point.y
        trans_to_point = Transformation.get_translation_matrix(x, y)
        scaling = Transformation.get_scaling_matrix(x_factor, y_factor)
        trans_back = Transformation.get_translation_matrix(-x, -y)
        return trans_to_point @ scaling @ trans_back

    def apply_translation(
        self, curr_matrix: np.array, data_input: Dict[str, str]
    ) -> np.array:
        """
        Method to apply translation matrix.
        It multiplies the current matrix by the translation from data input.

        Args:
            curr_matrix: current matrix (numpy array)
            data_input: dictionary with translation data

        Returns:
            resulting matrix (numpy array) aplying translation
        """

        result_matrix = curr_matrix

        trans_x = data_input["x"]
        if trans_x != "":
            result_matrix = result_matrix @ self.get_translation_matrix(
                float(trans_x), float(data_input["y"])
            )

        return result_matrix

    def apply_scale(
        self, curr_matrix, data_input: Dict[str, str], object: GraphicObject
    ) -> np.array:
        """
        Method to apply scaling matrix.
        It multiplies the current matrix by the scaling from data input and object center (anchor).

        Args:
            curr_matrix: current matrix (numpy array)
            data_input: dictionary with scaling data
            object: object reference to get center for anchoring scaling

        Returns:
            resulting matrix (numpy array) aplying scaling
        """
        result_matrix = curr_matrix

        x = data_input["x"]
        if x != "":
            result_matrix = result_matrix @ self.get_scaling_about_point(
                object.center, float(x), float(data_input["y"])
            )

        return result_matrix

    def apply_rotation(
        self, curr_matrix, data_input: Dict[str, str], object: GraphicObject
    ) -> np.array:
        """
        Method to apply rotation matrix.
        It multiplies the current matrix by the rotation from data input and object.

        Args:
            curr_matrix: current matrix (numpy array)
            data_input: dictionary with rotation data
            object: object reference to get data for anchoring rotation (if necessary)

        Returns:
            resulting matrix (numpy array) aplying rotation
        """
        result_matrix = curr_matrix

        angle = data_input["angle"]
        if angle != "":
            rotation_t = data_input["type"]
            match rotation_t:
                case RotationType.WORLD_CENTER:
                    result_matrix = result_matrix @ self.get_rotation_matrix(
                        float(angle)
                    )
                case RotationType.OBJECT_CENTER:
                    result_matrix = result_matrix @ self.get_rotation_about_point(
                        object.center, float(angle)
                    )
                case RotationType.AROUND_POINT:
                    anchor_point = tuple(data_input["point"])
                    print(anchor_point)
                    result_matrix = result_matrix @ self.get_rotation_about_point(
                        Point(float(anchor_point[0]), float(anchor_point[1])),
                        float(angle),
                    )
        return result_matrix

    def transform_object_points(
        self, object: GraphicObject, transform_input: Dict[TransformationType, Any]
    ) -> list[Point]:
        transforming_matrix = np.identity(3)

        transforming_matrix = self.apply_translation(
            transforming_matrix, transform_input[TransformationType.TRANSLATION]
        )
        transforming_matrix = self.apply_scale(
            transforming_matrix, transform_input[TransformationType.SCALING], object
        )
        transforming_matrix = self.apply_rotation(
            transforming_matrix, transform_input[TransformationType.ROTATION], object
        )

        new_points = self.transform_points(object.points, transforming_matrix)

        return new_points
