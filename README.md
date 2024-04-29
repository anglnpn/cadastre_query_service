# Сервис "CadastreCheck"

Разработан сервис, который обеспечивает доступ к результатам
проверки кадастровых данных. 
Сервис принимает запрос с указанием кадастрового номера, 
широты и долготы, эмулирует отправку запроса
на внешний сервер, который может обрабатывать запрос до 60 секунд и 
возвращает ответ 'True' или 'False'.

В сервисе доступен:

- просмотр результата по id запроса;
- просмотр истории всех запросов;
- просмотр истории по кадастровому номеру;

Стек: Python3, Django, DRF, Celery, pytest, Docker, PostgreSQL, Redis


## Запуск проекта:

1) Заполнить файл с переменными окружения .env.sample
и переименовать его в .env.docker
2) Запустить Docker Compose:

```
    docker-compose build
    
    docker-compose up
```

## Работа с сервисом:

1) Админка:

Доступна по адресу 
http://localhost:8001/admin/login/?next=/admin/

Для входа необходимо создать superuser

```
 docker-compose exec app python3 manage.py createsuperuser

```

2) Отправить запрос:

http://localhost:8001/main/query/

С POST запросом передать данные в формате json

```
{
    "number": "11:22:333333:444",
    "latitude": 90.0,
    "longitude": 180.0
}

```

3) Получить результат запроса:

http://localhost:8001/main/result/?id=1

В параметрах GET запроса указать id запроса 

4) Просмотреть историю всех запросов:

http://localhost:8001/main/history/

5) Просмотреть историю запросов по кадастровому номеру:

http://localhost:8001/main/history_number/?number=11:22:333333:444

В параметрах GET запроса указать number запроса

6) Проверить, что сервер запущен:

http://localhost:8001/main/ping/


## Запуск тестов:

```
docker-compose exec app poetry run pytest --cov

```

## Докуметация:

http://localhost:8001/swagger/
http://localhost:8001/redoc/
