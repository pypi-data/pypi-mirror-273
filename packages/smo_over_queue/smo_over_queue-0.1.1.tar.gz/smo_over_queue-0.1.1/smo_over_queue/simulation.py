from concurrent.futures import ProcessPoolExecutor, as_completed
from .models import Queue, Answer
from .exceptions import *
from .utils import round_value, sum_expected_values
from .processing import process_iteration

def simulate_queue(service_time: float, max_time: float, alpha: float, num_threads: int = 1, num_iterations: int = 1) -> Queue:
    """
    Симулирует работу очереди с указанными параметрами методом Монте-Карло.

    ### Параметры:
    * `service_time (float)` - Время обслуживания одной заявки.  
    * `max_time (float)` - Максимальное время симуляции.  
    * `alpha (float)` - Параметр для расчета интервала между заявками.  
    * `num_threads (int)` - Количество потоков (серверов) для обработки заявок. По умолчанию 1.  
    * `num_iterations (int)` - Количество итераций симуляции. По умолчанию 1.  

    ### Возвращаемое значение:
    Queue: Объект Queue, содержащий результаты симуляции и среднее количество обработанных заявок.

    ### Исключения:
    * `NumIterationsNegative` -  Если num_iterations < 0.
    * `NumIterationsIsZero` -  Если num_iterations == 0.
    * `NumThreadsNegative` -  Если num_threads < 0.
    * `NumThreadsIsZero` -  Если num_threads == 0.
    * `AlphaIsZero` -  Если alpha == 0.
    * `AlphaNegative` -  Если alpha < 0.
    * `ServiceTimeNegative` -  Если service_time < 0.
    * `MaxTimeNegative` -  Если max_time < 0.
    """
    
    # Проверка на отрицательное количество итераций
    if num_iterations < 0:
        raise NumIterationsNegative
    # Проверка на нулевое количество итераций
    elif num_iterations == 0:
        raise NumIterationsIsZero
    
    # Проверка на отрицательное количество потоков
    if num_threads < 0:
        raise NumThreadsNegative
    # Проверка на нулевое количество потоков
    elif num_threads == 0:
        raise NumThreadsIsZero
    
    # Проверка на нулевое значение alpha
    if alpha == 0:
        raise AlphaIsZero
    # Проверка на отрицательное значение alpha
    elif alpha < 0:
        raise AlphaNegative
    
    # Проверка на отрицательное время обслуживания
    if service_time < 0:
        raise ServiceTimeNegative

    # Проверка на отрицательное максимальное время
    if max_time < 0:
        raise MaxTimeNegative
    
    # Инициализация списка для хранения результатов каждой итерации
    answers: list[Answer] = []

    # Создание пула процессов для выполнения итераций параллельно
    with ProcessPoolExecutor() as executor:
        # Создание задач для каждой итерации
        futures = [executor.submit(process_iteration, service_time, max_time, alpha, num_threads) for _ in range(num_iterations)]
        
        # Обработка результатов по мере завершения задач
        for future in as_completed(futures):
            answers.append(future.result())
    
    # Возвращение объекта Queue с результатами и средним значением обработанных заявок
    return Queue(answers, round_value(sum_expected_values(answers) / len(answers)))