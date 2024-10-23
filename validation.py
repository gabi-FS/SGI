import re
from typing import List, Tuple

from globals import ObjectType, RotationType, TransformationType


class ValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class Validation:
    """Levanta exceções quando recebe valores considerados inválidos. Não transforma entradas."""

    # TODO: Se necessário, criar lógica análoga a throwIfInvalid para melhorar legibilidade

    @staticmethod
    def object_coordinates_input(
        input_list: List[Tuple[float, float]] | List[Tuple[float, float, float]],
        object_type: ObjectType,
    ):
        if len(input_list) == 0:
            raise ValidationError("Nenhuma tupla foi encontrada.")

        match object_type:
            case ObjectType.LINE:
                if len(input_list) < 2:
                    raise ValidationError(
                        "É necessário que uma linha possua mais que uma coordenada."
                    )
            case ObjectType.WIREFRAME_POLYGON:
                if len(input_list) < 2:
                    raise ValidationError(
                        "É necessário que um polígono possua mais que uma coordenada."
                    )
            case ObjectType.FILLED_POLYGON:
                if len(input_list) < 2:
                    raise ValidationError(
                        "É necessário que um polígono possua mais que uma coordenada."
                    )

    @staticmethod
    def object_transform_input(object_input: dict):
        """Aceita valores vazios, exceto para conjunto ângulo e ponto para tipo de rotação ao redor do ponto
        (os dois devem ser preenchidos ou os dois devem ser vazios)
        """
        try:
            for key, value in object_input.items():
                match key:
                    case TransformationType.TRANSLATION:
                        Validation._translation(value)
                    case TransformationType.ROTATION:
                        Validation._rotation(value)
                    case TransformationType.SCALING:
                        Validation._scaling(value)
        except ValidationError as e:  # Repassa exceções
            raise ValidationError(e)

    @staticmethod
    def _validate_xyz(input_object: dict[str, str], error_message: str):
        x, y, z = (
            input_object["x"].strip(),
            input_object["y"].strip(),
            input_object["z"].strip(),
        )
        try:
            if x != "":
                float(x)
            if y != "":
                float(y)
            if z != "":
                float(z)
            return x, y, z
        except ValueError:
            raise ValidationError(error_message)

    @staticmethod
    def _translation(input_object: dict[str, str]):
        Validation._validate_xyz(
            input_object,
            error_message="Os valores de translação precisam ser numéricos",
        )

    @staticmethod
    def _rotation(input_object: dict):
        x, y, z = Validation._validate_xyz(
            input_object,
            error_message="O valor do ângulo precisa ser numérico",
        )
        type_value = input_object["type"]

        if RotationType.AROUND_POINT == type_value:
            point_value = input_object["point"].strip()
            if x != "" or y != "" or z != "":
                if point_value == "":
                    raise ValidationError(
                        "O ponto precisa ser preenchido caso o ângulo seja preenchido para esse tipo de rotação."
                    )

                tuple_pattern = r"\(([^)]+)\)"
                matches = re.findall(tuple_pattern, point_value)
                if len(matches) != 1:
                    raise ValidationError("A entrada de ponto precisa de uma tupla.")
                numbers = matches[0].split(",")
                if len(numbers) != 3:
                    raise ValidationError(
                        f"Tupla inválida (deve conter exatamente três elementos): {matches[0]}"
                    )
                try:
                    float(numbers[0].strip())
                    float(numbers[1].strip())
                    float(numbers[2].strip())
                except ValueError:
                    raise ValidationError(
                        "Os valores da tupla de pontos precisam ser numéricos"
                    )
            elif point_value != "":
                raise ValidationError(
                    "Ângulo deve ser preenchido caso o ponto seja para esse tipo de rotação."
                )

    @staticmethod
    def _scaling(input_object: dict):
        x, y, z = Validation._validate_xyz(
            input_object,
            error_message="Os valores de escalonamento precisam ser numéricos",
        )
