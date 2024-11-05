from typing import Any, Dict

import numpy as np

from globals import RotationType, TransformationType, TranslationType
from system.basics import Point
from system.objects import GraphicObject
from utils import get_tuple_from_object, get_tuple_from_str


class Transformation:
    _normalizing_matrix: np.array

    def __init__(self) -> None:
        self._normalizing_matrix = np.identity(4)

    @property
    def normalizing_matrix(self):
        return self._normalizing_matrix

    @staticmethod
    def get_transformed_points(
        graphic_object: GraphicObject,
        transform_input: Dict[TransformationType, Any],
        window_rotation: np.array,
        window_center: Point,
    ) -> list[Point]:
        """
        Dada a entrada e os dados do objeto, retorna novos pontos com as transformações aplicadas.
        """
        identity_matrix = np.identity(4)
        transforming_matrix = identity_matrix

        transforming_matrix = Transformation.apply_translation(
            transforming_matrix,
            transform_input[TransformationType.TRANSLATION],
            window_rotation,
            window_center,
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
        curr_matrix: np.array,
        data_input: Dict[str, str],
        window_rotation: np.array = None,
        window_center: Point = None,
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
            x, y, z = get_tuple_from_object(data_input, 0)
        except ValueError:
            return curr_matrix

        trans_type = data_input["type"]
        if trans_type == TranslationType.SCREEN_AXIS:

            translate_back_from_origin = Transformation.get_translation_matrix(
                window_center.x, window_center.y, window_center.z
            )
            rotate_again = window_rotation
            translate_amount = Transformation.get_translation_matrix(x, y, z)
            undo_rotation = np.linalg.inv(window_rotation)
            translate_back_to_origin = Transformation.get_translation_matrix(
                -window_center.x, -window_center.y, -window_center.z
            )

            translation_matrix = (
                translate_back_from_origin
                @ undo_rotation
                @ translate_amount
                @ rotate_again
                @ translate_back_to_origin
            )

        else:
            translation_matrix = Transformation.get_translation_matrix(x, y, z)

        return curr_matrix @ translation_matrix

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
            (x, y, z) = get_tuple_from_object(data_input, 1)
        except ValueError:
            return curr_matrix
        return curr_matrix @ Transformation.get_scaling_about_point(
            object_center, x, y, z
        )

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
        try:
            x, y, z = get_tuple_from_object(data_input)
        except ValueError:
            return curr_matrix

        rotation_type = data_input["type"]
        x_angle = np.deg2rad(x)
        y_angle = np.deg2rad(y)
        z_angle = np.deg2rad(z)

        match rotation_type:
            case RotationType.WORLD_CENTER:
                rotation_matrix = Transformation.get_rotation_matrix(
                    x_angle, y_angle, z_angle
                )
            case RotationType.OBJECT_CENTER:
                rotation_matrix = Transformation.get_rotation_about_point(
                    object_center, x_angle, y_angle, z_angle
                )
            case RotationType.AROUND_POINT:
                numbers = get_tuple_from_str(data_input["point"])
                rotation_matrix = Transformation.get_rotation_about_point(
                    Point(*numbers), x_angle, y_angle, z_angle
                )
        return curr_matrix @ rotation_matrix

    @staticmethod
    def transform_points(points: list[Point], matrix: np.array) -> list[Point]:
        result = []
        for point in points:
            coord = matrix @ np.array(point.get_homogeneous_matrix())
            print(coord)
            new_point = Point(coord[0, 0], coord[1, 0], coord[2, 0])
            result.append(new_point)
        return result

    @staticmethod
    def get_rotation_about_axis(
        point: Point, axis: Point, rotation_angle: float
    ) -> np.array:
        """
        Method to build a rotation matrix about an axis.

        Args:
            point: point of reference to the rotation
            rotation_angle: rotation angle in rad

        Returns:
            rotation matrix (numpy array)
        """
        x, y, z = point.x, point.y, point.z

        x_axis = Point(1, 0, 0)
        x_angle = Point.angle_between_vectors(x_axis, axis)
        z_axis = Point(0, 0, 1)
        z_angle = Point.angle_between_vectors(z_axis, axis)

        # levar até a origem
        trans_to_point = Transformation.get_translation_matrix(x, y, z)

        # rotacionar para alinhar ao plano xy
        rotation_x = Transformation.get_rotation_matrix_x(x_angle)
        rotation_z = Transformation.get_rotation_matrix_z(z_angle)

        # rotacionar de acordo com o ângulo desejado
        true_rotation = Transformation.get_rotation_matrix_y(rotation_angle)

        # trazer de volta para o lugar original e desfazer rotações
        trans_back = Transformation.get_translation_matrix(-x, -y, -z)
        undo_rotation_x = Transformation.get_rotation_matrix_x(-x_angle)
        undo_rotation_z = Transformation.get_rotation_matrix_z(-z_angle)

        return (
            trans_to_point
            @ rotation_x
            @ rotation_z
            @ true_rotation
            @ undo_rotation_z
            @ undo_rotation_x
            @ trans_back
        )

    @staticmethod
    def get_rotation_about_point(
        point: Point, x_angle: float, y_angle: float, z_angle: float
    ) -> np.array:
        """
        Method to build a rotation matrix about an axis.

        Args:
            point: point of reference to the rotation
            rotation_angle: rotation angle in rad

        Returns:
            rotation matrix (numpy array)
        """
        x, y, z = point.x, point.y, point.z

        # levar até a origem
        trans_to_point = Transformation.get_translation_matrix(x, y, z)

        rotation = Transformation.get_rotation_matrix(x_angle, y_angle, z_angle)

        # trazer de volta para o lugar original e desfazer rotações
        trans_back = Transformation.get_translation_matrix(-x, -y, -z)

        return trans_to_point @ rotation @ trans_back

    @staticmethod
    def get_rotation_matrix(x_angle: float, y_angle: float, z_angle: float) -> np.array:
        """
        Method to build a 3D rotation matrix.

        Args:
            rotation_angle: rotation angle in rad

        Returns:
            rotation matrix (numpy array)
        """
        rotation_x = Transformation.get_rotation_matrix_x(x_angle)
        rotation_y = Transformation.get_rotation_matrix_y(y_angle)
        rotation_z = Transformation.get_rotation_matrix_z(z_angle)
        return rotation_x @ rotation_y @ rotation_z

    @staticmethod
    def get_scaling_about_point(
        point: Point,
        x_factor: float,
        y_factor: float,
        z_factor: float,
        rotation_matrix: np.array = np.identity(4),
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
        x, y, z = point.x, point.y, point.z
        trans_back = Transformation.get_translation_matrix(x, y, z)
        scaling = Transformation.get_scaling_matrix(x_factor, y_factor, z_factor)
        trans_to_point = Transformation.get_translation_matrix(-x, -y, -z)
        return (
            trans_back
            @ rotation_matrix
            @ scaling
            @ np.linalg.inv(rotation_matrix)
            @ trans_to_point
        )

    @staticmethod
    def get_scaling_matrix(
        x_factor: float, y_factor: float, z_factor: float
    ) -> np.array:
        """
        Method to build a scaling matrix.

        Args:
            x_factor: scaling factor in x-axis
            y_factor: scaling factor in y-axis
            z_factor: scaling factor in z-axis

        Returns:
            scaling matrix (numpy array)
        """
        return np.array(
            [
                [x_factor, 0, 0, 0],
                [0, y_factor, 0, 0],
                [0, 0, z_factor, 0],
                [0, 0, 0, 1],
            ]
        )

    @staticmethod
    def get_translation_matrix(
        x_factor: float, y_factor: float, z_factor: float
    ) -> np.array:
        """
        Method to build a translation matrix.

        Args:
            x_factor: translation factor in x-axis
            y_factor: translation factor in y-axis
            z_factor: translation factor in z-axis

        Returns:
            translation matrix (numpy array)
        """
        return np.array(
            [
                [1, 0, 0, x_factor],
                [0, 1, 0, y_factor],
                [0, 0, 1, z_factor],
                [0, 0, 0, 1],
            ]
        )

    @staticmethod
    def get_rotation_matrix_x(angle: float) -> np.array:
        """
        Method to build a rotation matrix about x axis.

        Args:
            angle: rotation angle in rad

        Returns:
            rotation matrix (numpy array)
        """
        cos = np.cos(angle)
        sin = np.sin(angle)
        return np.array(
            [
                [1, 0, 0, 0],
                [0, cos, -sin, 0],
                [0, sin, cos, 0],
                [0, 0, 0, 1],
            ]
        )

    @staticmethod
    def get_rotation_matrix_y(angle: float) -> np.array:
        """
        Method to build a rotation matrix about y axis.

        Args:
            angle: rotation angle in rad

        Returns:
            rotation matrix (numpy array)
        """
        cos = np.cos(angle)
        sin = np.sin(angle)
        return np.array(
            [
                [cos, 0, sin, 0],
                [0, 1, 0, 0],
                [-sin, 0, cos, 0],
                [0, 0, 0, 1],
            ]
        )

    @staticmethod
    def get_rotation_matrix_z(angle: float) -> np.array:
        """
        Method to build a rotation matrix about z axis

        Args:
            angle: rotation angle in rad

        Returns:
            rotation matrix (numpy array)
        """
        cos = np.cos(angle)
        sin = np.sin(angle)

        return np.array(
            [
                [cos, -sin, 0, 0],
                [sin, cos, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )

    def set_normalizing_matrix(self, window, cop_distance=1) -> np.array:
        """Normaliza considerando projeção em perspectiva"""

        window_size = Point.size(window.points[0], window.points[3])
        x, y, z = window.center

        tr_to_origin = Transformation.get_translation_matrix(-x, -y, -z)
        rotate = window.rotation_matrix
        tr_cop_to_origin = Transformation.get_translation_matrix(
            0, 0, cop_distance * (window_size / 2)
        )
        scale = Transformation.get_scaling_matrix(
            window.scale_x, window.scale_y, 2 / window_size
        )
        print(window.scale_x, window.scale_y, 2 / window_size)
        print(window_size)
        print()

        #  As transformações são aplicadas na ordem invertida
        self._normalizing_matrix = scale @ tr_cop_to_origin @ rotate @ tr_to_origin
        return self._normalizing_matrix
