class NumIterationsNegative(Exception):
    """
    Исключение выбрасывается, если количество итераций отрицательное.
    """
    pass

class NumIterationsIsZero(Exception):
    """
    Исключение выбрасывается, если количество итераций равно нулю.
    """
    pass

class NumThreadsNegative(Exception):
    """
    Исключение выбрасывается, если количество потоков отрицательное.
    """
    pass

class NumThreadsIsZero(Exception):
    """
    Исключение выбрасывается, если количество потоков равно нулю.
    """
    pass

class AlphaIsZero(Exception):
    """
    Исключение выбрасывается, если параметр alpha равен нулю.
    """
    pass

class AlphaNegative(Exception):
    """
    Исключение выбрасывается, если параметр alpha отрицательный.
    """
    pass

class ServiceTimeNegative(Exception):
    """
    Исключение выбрасывается, если время обслуживания отрицательное.
    """
    pass

class MaxTimeNegative(Exception):
    """
    Исключение выбрасывается, если максимальное время симуляции отрицательное.
    """
    pass
