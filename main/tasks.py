import time
import random
from celery import shared_task
from django.conf import settings

from main.models import Query
from main.utils import random_response


@shared_task
def simulating_server_response(id_query):
    """
    Получает id запроса.
    Записывает 'True'/'False' в поле 'server_response'
    объекта 'Query' и сохраняет в БД.
    Эмулирует ответ сервера c
    задержкой от 1 до 60с.
    """

    time.sleep(random.randint(1, 60))

    query_obj = Query.objects.get(id=id_query)
    query_obj.server_response = random_response()
    query_obj.save()