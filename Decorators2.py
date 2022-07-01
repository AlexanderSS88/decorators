from functools import wraps
import os
from datetime import datetime

def logger(path):
    def dec_logger(func):
        def wrapped(*args, **kwargs):
            key = f'позиционные аргументы: {args}, именованные аргументы: {kwargs}'
            data = {}

            print('*' * 50)
            time_start = datetime.now()
            result = func(*args, **kwargs)
            time_end = datetime.now()
            print('*' * 50)

            data['Название функции: '] = func.__name__
            data['Аргументы функции: '] = key
            data['Время начала работы функции: '] = time_start.isoformat()
            data['Возвращаемое значение функции '] = result
            data['Время окончания работы функции: '] = time_end.isoformat()

            with open(path, "w+") as my_log:
                for position in data.items():
                    x, y = position
                    my_log.write(f"{x} {y} \n")
            return result
        return wrapped
    return dec_logger


