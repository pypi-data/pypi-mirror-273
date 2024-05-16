import math
import random

from smo_over_queue.models import Answer

from typing import TypeVar

T = TypeVar('T')

def round_value(value: float | int, decimals: int = 4) -> float:
    """
    Округляет значение до указанного количества десятичных знаков.

    ### Параметры:
    * `value (float)`: Число для округления.
    * `decimals (int)`: Количество знаков после запятой. По умолчанию 4.

    ### Возвращает:
    `float`: Округленное значение.
    """
    return round(value, decimals)

def interval_between_apps(alpha, random_value):
    """
    Вычисляет интервал между заявками на основе параметра alpha и случайного значения.

    ### Параметры:
    * `alpha (float)`: Параметр для расчета интервала между заявками.
    * `random_value (float)`: Случайное значение, использованное в расчете.

    ### Возвращает:
    `float`: Округленный интервал между заявками.
    """
    return round_value(-1 / alpha * math.log(random_value))

def max_row(lst: list[T]) -> T:
    """
    Возвращает максимальное значение в списке.

    ### Параметры:
    `lst (list)`: Список чисел.

    ### Возвращает:
    `float`: Максимальное значение в списке.
    """
    return max(lst)

def transpose(matrix: list[list[T]]) -> list[list[T]]:
    """
    Транспонирует матрицу, заменяя строки на столбцы.

    ### Параметры:
    `matrix (list[list])`: Двумерный список (матрица).

    ### Возвращает:
    `list[list]`: Транспонированная матрица.
    """
    rows = len(matrix)
    cols = len(matrix[0])
    transposed_matrix = []

    for col in range(cols):
        new_row = []
        for row in range(rows):
            new_row.append(matrix[row][col])
        transposed_matrix.append(new_row)

    return transposed_matrix

def max_columns(lst: list[list[T]]) -> list[T]:
    """
    Возвращает список максимальных значений для каждого столбца матрицы.

    ### Параметры:
    `lst (list[list])`: Двумерный список (матрица).

    ### Возвращает:
    `list`: Список максимальных значений для каждого столбца.
    """
    return [max_row(row) for row in transpose(lst)]

def generate_random_number():
    """
    Генерирует случайное число в диапазоне (0, 1] с округлением до 4 знаков после запятой.
    Если сгенерировано 0, повторяет генерацию.

    ### Возвращает:
    `float`: Случайное число в диапазоне (0, 1].
    """
    number = round_value(random.uniform(0, 1))
    if number == 0:
        return generate_random_number()
    else:
        return number

def sum_expected_values(lst: list[Answer]):
    """
    Вычисляет сумму ожидаемых значений из списка объектов Answer.

    ### Параметры:
    `lst (list[Answer])`: Список объектов Answer.

    ### Возвращает:
    `float`: Сумма ожидаемых значений.
    """
    return sum([answer.expected_value for answer in lst])
