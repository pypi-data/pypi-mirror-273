from smo_over_queue.models import Iteration, Answer
from smo_over_queue.utils import round_value, interval_between_apps, max_columns, generate_random_number

def process_iteration(service_time: float, max_time: float, alpha: float, num_threads: int) -> Answer:
    """
    Обрабатывает одну итерацию симуляции очереди с заданными параметрами.

    ### Параметры:
    * `service_time (float)` - Время обслуживания одной заявки.
    * `max_time (float)` - Максимальное время симуляции.
    * `alpha (float)` - Параметр для расчета интервала между заявками.
    * `num_threads (int)` - Количество потоков (серверов) для обработки заявок.

    ### Возвращает:
    `Answer` - Объект Answer, содержащий результаты итерации и количество обработанных заявок.

    ### Описание:
    Функция симулирует процесс обработки заявок в `СМО` с `неограниченной очередью`. 
    
    Для каждой итерации рассчитываются интервалы между поступлением заявок, время обслуживания, 
    и распределение заявок по серверам. Результаты каждой итерации сохраняются в объекте `Iteration` 
    и возвращаются в виде объекта `Answer`.
    """
    iterations: list[Iteration] = []  # Список для хранения данных каждой итерации
    current_time = 0  # Текущее время в симуляции
    random_value = 0  # Случайное значение для расчета интервала между заявками
    interval = 0  # Интервал между заявками
    servers: list[list[float]] = []  # Список для хранения времени занятости каждого сервера
    server_row_count = 0  # Счетчик строк для сервера
    application_count = 0  # Счетчик обработанных заявок

    while current_time <= max_time:
        # Добавляем новую строку для серверов и инициализируем ее нулями
        servers.append([0] * num_threads)
        column_max_values = max_columns(servers)  # Максимальные значения по столбцам (время завершения работы серверов)

        for index, value in enumerate(column_max_values):
            if current_time >= value:
                # Если текущее время больше или равно времени завершения работы сервера, назначаем новый интервал
                servers[server_row_count][index] = round_value(current_time + service_time)
                break
        else:
            if index + 1 < len(servers[server_row_count]):
                # Если есть свободные серверы, назначаем время обслуживания
                servers[server_row_count][index + 1] = round_value(current_time + service_time)
            else:
                # Иначе ждем, пока один из серверов освободится
                min_column_max = min(column_max_values)
                current_time = min_column_max
                servers[server_row_count][column_max_values.index(min_column_max)] = round_value(current_time + service_time)

        server_row_count += 1

        # Сохраняем данные текущей итерации
        iterations.append(
            Iteration(
                index=application_count,
                random_value=random_value,
                interval_between_apps=interval,
                application_time=current_time,
                server_times=servers[-1]
            )
        )

        # Генерируем новое случайное значение и рассчитываем новый интервал между заявками
        random_value = generate_random_number()
        interval = interval_between_apps(alpha, random_value)
        current_time = round_value(current_time + interval)
        application_count += 1

    return Answer(iterations[:], application_count - 1)
