import re
from typing import Dict, List, Tuple

# TODO: métodos podem ser mais genéricos e também criados para serem utilizados nas funções de validação, se necessário

TUPLE_PATTERN = r"\(([^)]+)\)"


def parse_input(
    input_str: str,
) -> List[Tuple[float, float]] | List[Tuple[float, float, float]]:
    matches = re.findall(TUPLE_PATTERN, input_str)
    result = []
    for match in matches:
        numbers = match.split(",")
        # a tupla pode conter 2 ou 3 elementos
        if len(numbers) not in (2, 3):  # TODO: Separar parsing e validação
            raise ValueError(f"Tupla inválida (deve conter 2 ou 3 elementos): {match}")
        try:
            numbers_tuple = []  # inicializar a tupla de números como uma lista
            for num in numbers:
                numbers_tuple.append(float(num.strip()))

            # transformar a lista em uma tupla propriamente dita
            numbers_tuple = tuple(numbers_tuple)

            result.append(numbers_tuple)
            print(result)
        except ValueError:
            raise ValueError(
                f"Os valores fornecidos na tupla não são números válidos: {match}"
            )
    return result


def get_tuple_from_str(string: str) -> Tuple[float, float]:
    """a single tuple with two numbers from a string in (number, number) format"""
    matches = re.findall(TUPLE_PATTERN, string)
    number1, number2 = matches[0].split(",")
    return float(number1.strip()), float(number2.strip())


def get_tuple_from_object(
    data_input: Dict[str, str], default_value: int = 0
) -> Tuple[float, float]:
    """_summary_
    Args:
        data_input (Dict[str, str]): objeto que possui chaves "x" e "y"
        default_value (int, optional): substitui o valor de um dos números caso ele não exista.

    Raises:
        ValueError: Os dois valores (x e y) estão vazios.
    """
    input_x, input_y = data_input["x"].strip(), data_input["y"].strip()
    if input_x == "" and input_y == "":
        raise ValueError("Os dois valores estão vazios")
    elif input_x == "" and input_y != "":
        x, y = default_value, float(input_y)
    elif input_x != "" and input_y == "":
        x, y = float(input_x), default_value
    else:
        x, y = float(input_x), float(input_y)
    return x, y
