from functools import wraps
from datetime import datetime


def decorator_logger(old_function):
    data = {}
    @wraps(old_function)
    def new_function(*args, **kwargs):
        key = f'позиционные аргументы: {args}, именованные аргументы: {kwargs}'

        print('*' * 100)
        time_start = datetime.now()
        result = old_function(*args, **kwargs)
        time_end = datetime.now()
        print('*' * 100)

        data['Название функции: '] = old_function.__name__
        data['Аргументы функции: '] = key
        data['Время начала работы функции: '] = time_start.isoformat()
        data['Возвращаемое значение функции '] = result
        data['Время окончания работы функции: '] = time_end.isoformat()

        with open("data.log", "w+") as my_log:
            for position in data.items():
                x, y = position
                my_log.write(f"{x} {y} \n")
        return result
    return new_function


