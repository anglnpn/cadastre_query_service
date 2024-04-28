import pytest

from rest_framework import status
from rest_framework.test import APIClient

from main.models import Query

client = APIClient()


@pytest.fixture
def test_url_create():
    return '/main/query/'


@pytest.fixture
def test_url_list():
    return '/main/history/'


@pytest.fixture
def test_url_number_list():
    return '/main/history_number/'


@pytest.fixture
def test_url_result():
    return '/main/result/'


@pytest.mark.django_db
def test_query_create(test_url_create):
    """
    Тест для проверки успешного
     создания запроса.
    """
    url = test_url_create
    data = {
        'number': '77:77:88888:999',
        'latitude': 90.00,
        'longitude': 180.00
    }

    response = client.post(url, data)

    query_from_db = Query.objects.get(number=data['number'])

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'message': 'Запрос по кадастровому номеру: '
                   '77:77:88888:999 отправлен. id запроса: 1. '
                   'Ожидайте ответ сервера.'
    }
    assert data['number'] == query_from_db.number
    assert data['latitude'] == query_from_db.latitude
    assert data['longitude'] == query_from_db.longitude


@pytest.mark.django_db
def test_bad_request_number(test_url_create):
    """
    Тест для проверки некорректного
    запроса.
    Нет ключа 'number'.
    """
    url = test_url_create
    data = {
        'latitude': 90.00,
        'longitude': 180.00
    }

    response = client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"number": ["Обязательное поле."]}


@pytest.mark.django_db
def test_bad_request_latitude(test_url_create):
    """
    Тест для проверки некорректного
    запроса.
    Нет ключа 'latitude'.
    """
    url = test_url_create
    data = {
        'number': '77:77:88888:999',
        'longitude': 180.00
    }

    response = client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"latitude": ["Обязательное поле."]}


@pytest.mark.django_db
def test_bad_request_longitude(test_url_create):
    """
    Тест для проверки некорректного
    запроса.
    Нет ключа 'longitude'.
    """
    url = test_url_create
    data = {
        'number': '77:77:88888:999',
        'latitude': 90.00
    }

    response = client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"longitude": ["Обязательное поле."]}


@pytest.mark.django_db
def test_bad_request_number_format(test_url_create):
    """
    Тест для проверки некорректного
    запроса.
    Некорректный формат кадастрового номера.
    """
    url = test_url_create
    data = {
        'number': '77:77:88888:',
        'latitude': 90.00,
        'longitude': 180.00
    }

    response = client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'non_field_errors': ['Неверный формат кадастрового номера. '
                             'Введите номер в формате: АА:ВВ:CCCCСCC:КК, '
                             'где: '
                             'АА – кадастровый округ; '
                             'ВВ - кадастровый район; '
                             'CCCCCCС - кадастровый квартал в пределах '
                             'данного кадастрового района  (состоит из 7 цифр); '
                             'КК – уникальный номер объекта.']
    }


@pytest.mark.django_db
def test_bad_request_latitude_format(test_url_create):
    """
    Тест для проверки некорректного
    запроса.
    Некорректный формат широты.
    """
    url = test_url_create
    data = {
        'number': '77:77:88888:999',
        'latitude': 900.00,
        'longitude': 180.00
    }

    response = client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'non_field_errors': ['Неверный формат широты. '
                             'Введите широту в диапазоне от -90 до 90.']
    }


@pytest.mark.django_db
def test_bad_request_longitude_format(test_url_create):
    """
    Тест для проверки некорректного
    запроса.
    Некорректный формат долготы.
    """
    url = test_url_create
    data = {
        'number': '77:77:88888:999',
        'latitude': 90.00,
        'longitude': 1800.00
    }

    response = client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'non_field_errors': ['Неверный формат долготы. '
                             'Введите долготу в диапазоне от -180 до 180.']
    }


@pytest.mark.django_db
def test_bad_request_empty(test_url_create):
    """
    Тест для проверки некорректного
    запроса.
    Пустой запрос.
    """
    url = test_url_create
    data = {}

    response = client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'number': ['Обязательное поле.'],
        'latitude': ['Обязательное поле.'],
        'longitude': ['Обязательное поле.']
    }


@pytest.mark.django_db
def test_query_list(test_url_list):
    """
    Тест для проверки успешного
     получения списка запросов.
    """
    Query.objects.create(
        number='77:77:88888:999',
        latitude=90.0,
        longitude=180.0)
    Query.objects.create(
        number='77:77:88888:111',
        latitude=90.0,
        longitude=180.0)

    url = test_url_list

    response = client.get(url)
    print(response.data)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_query_list_empty(test_url_list):
    """
    Тест для проверки получения
    пустого списка запросов.
    """
    url = test_url_list

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


@pytest.mark.django_db
def test_query_list_bad_request(test_url_list):
    """
    Тест для проверки некорректного
    запроса.
    """
    url = test_url_list
    data = {
        'id': 1
    }

    response = client.post(url, data)

    assert response.status_code == 405


@pytest.mark.django_db
def test_query_list_number(test_url_number_list):
    """
    Тест для проверки корректного запроса
    истории запросов по кадастровому номеру.
    """
    Query.objects.create(
        number='11:77:88888:999',
        latitude=90.0,
        longitude=180.0)
    Query.objects.create(
        number='11:77:88888:999',
        latitude=90.0,
        longitude=180.0)

    url = test_url_number_list

    response = client.get(url + '?number=11:77:88888:999')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_query_list_number_bad(test_url_number_list):
    """
    Тест для проверки некорректного запроса
    истории запросов по кадастровому номеру.
    """
    url = test_url_number_list

    response = client.get(url + '?number=22:77:88888:999')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "message": "По данному кадастровому номеру запросы не найдены"
    }


@pytest.mark.django_db
def test_query_result(test_url_result):
    """
    Тест для проверки корректного запроса
    для получения результата запроса на сервер.
    """
    Query.objects.create(
        number='11:22:3333:4444',
        latitude=90.0,
        longitude=180.0)

    query = Query.objects.get(number='11:22:3333:4444')
    id_query = query.id

    url = test_url_result

    response = client.get(url + f'?id={id_query}')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        'message': 'Статус запроса: ожидает ответ сервера'}


@pytest.mark.django_db
def test_query_result_bad(test_url_result):
    """
    Тест для проверки некорректного запроса
    для получения результата запроса на сервер.
    """
    url = test_url_result

    response = client.get(url + '?id=a')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_server_ping():
    """
    Тест для проверки корректного запроса
    на сервер.
    """
    url = '/main/ping/'

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"message": "Сервер доступен"}
