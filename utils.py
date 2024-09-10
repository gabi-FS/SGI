import re
from typing import List, Tuple

from globals import ObjectType

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
