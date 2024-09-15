import re
from typing import List, Tuple

from globals import ObjectType, RotationType, TransformationType

""" Adicionar quaisquer funções úteis utilizados que não necessitem de classe específica neste arquivo"""


def parse_input(input_str: str) -> List[Tuple[float]]:
    tuple_pattern = r"\(([^)]+)\)"
    matches = re.findall(tuple_pattern, input_str)
    result = []
    for match in matches:
        numbers = match.split(',')
        if len(numbers) != 2:
            raise ValueError(
                f"Tupla inválida (deve conter exatamente dois elementos): {match}")
        try:
            num1 = float(numbers[0].strip())
            num2 = float(numbers[1].strip())
            result.append((num1, num2))
        except ValueError:
            raise ValueError(
                f"Os valores fornecidos na tupla não são números válidos: {match}")

    return result


def validate(input_list: List[Tuple[float]], object_type: ObjectType):
    """ Demais validações, com o propósito de não causar erros ao sistema """

    if len(input_list) == 0:
        raise ValueError("Nenhuma tupla foi encontrada.")

    match object_type:
        case ObjectType.LINE:
            if len(input_list) < 2:
                raise ValueError(
                    "É necessário que uma linha possua mais que uma coordenada.")
        case ObjectType.POLYGON:
            if len(input_list) < 2:
                raise ValueError(
                    "É necessário que um polígono possua mais que uma coordenada.")


def validate_transform_input(object_input: dict):
    ''' Aceita valores vazios, 
    exceto para conjunto ângulo e ponto para tipo de rotação ao redor do ponto 
    (os dois devem ser preenchidos ou os dois devem ser vazios)

    '''
    try:
        for key, value in object_input.items():
            match key:
                case TransformationType.TRANSLATION:
                    validate_translation(value)
                case TransformationType.ROTATION:
                    validate_rotation(value)
                case TransformationType.SCALING:
                    validate_scaling(value)
    except (ValueError) as e:  # Repassa exceções
        raise ValueError(e)


def validate_translation(object: dict[str, str]):
    x_value = object['x']
    y_value = object['y']
    try:
        if x_value.strip() != '':
            float(x_value.strip())
        if y_value.strip() != '':
            float(y_value.strip())
    except ValueError:
        raise ValueError("Os valores de translação precisam ser numéricos")


def validate_rotation(object: dict):
    type_value = object['type']
    angle_value = object['angle']

    try:
        if angle_value.strip() != '':
            float(angle_value)
    except ValueError:
        raise ValueError("O valor do ângulo precisa ser numérico")

    if RotationType.AROUND_POINT == type_value:
        point_value = object['point']
        if angle_value.strip() != '':
            if point_value.strip() == '':
                raise ValueError(
                    "O ponto precisa ser preenchido caso o ângulo seja preenchido para esse tipo de rotação.")

            tuple_pattern = r"\(([^)]+)\)"
            matches = re.findall(tuple_pattern, point_value)
            if len(matches) != 1:
                raise ValueError("A entrada de ponto precisa de uma tupla.")
            numbers = matches[0].split(',')
            if len(numbers) != 2:
                raise ValueError(
                    f"Tupla inválida (deve conter exatamente dois elementos): {matches[0]}")
            try:
                float(numbers[0].strip())
                float(numbers[1].strip())
            except ValueError:
                raise ValueError(
                    "Os da tupla de pontos precisam ser numéricos")

        elif point_value.strip() != '':
            raise ValueError(
                "Ângulo deve ser preenchido caso o ponto seja para esse tipo de rotação.")


def validate_scaling(object: dict):
    # TODO: Avaliar se aceita valores negativos.
    x_value = object['x']
    y_value = object['y']
    try:
        if x_value.strip() != '':
            float(x_value.strip())
        if y_value.strip() != '':
            float(y_value.strip())
    except ValueError:
        raise ValueError("Os valores de escalonamento precisam ser numéricos")
