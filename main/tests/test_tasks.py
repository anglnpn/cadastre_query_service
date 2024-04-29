import pytest

from main.models import Query
from main.tasks import simulating_server_response


@pytest.mark.django_db
def test_simulating_server_response():
    """
    Тестирование задачи simulating_server_response.
    """
    # Создаем объект запроса
    query_obj = Query.objects.create(
        number='11:22:3333:4444',
        latitude=90.0,
        longitude=180.0
    )

    # Вызываем задачу
    result = simulating_server_response.delay(query_obj.id)

    assert result.state == 'PENDING'
