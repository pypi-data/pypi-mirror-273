from dataclasses import dataclass

@dataclass
class Iteration:
    """
    Класс для хранения информации об одной итерации симуляции.

    ### Атрибуты:
    * `index (int)` - Индекс итерации.
    * `random_value (float)` - Случайное значение, использованное для расчета интервала между заявками.
    * `interval_between_apps (float)` - Расчетный интервал между заявками.
    * `application_time (float)` - Время поступления заявки.
    * `server_times (list[float])` - Время занятости серверов (потоков) на момент поступления заявки.
    """
    index: int
    random_value: float
    interval_between_apps: float
    application_time: float
    server_times: list[float]

@dataclass
class Answer:
    """
    Класс для хранения результатов одной итерации симуляции очереди.

    ### Атрибуты:
    * `iterations (list[Iteration])` - Список объектов Iteration, представляющих каждую обработанную заявку.
    * `expected_value (float)` - Ожидаемое значение (например, количество обработанных заявок).
    """
    iterations: list[Iteration]
    expected_value: float

@dataclass
class Queue:
    """
    Класс для хранения результатов всех итераций симуляции очереди и среднего значения.

    ### Атрибуты:
    * `results (list[Answer])` - Список объектов Answer, представляющих результаты каждой итерации.
    * `average_value (float)` - Среднее значение (например, среднее количество обработанных заявок) по всем итерациям.
    """
    results: list[Answer]
    average_value: float
