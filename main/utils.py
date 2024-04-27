import random

foo = [True, False]


def random_response():
    """
    Функция возвращает случайный ответ
    сервера.
    """
    return random.choice(foo)
