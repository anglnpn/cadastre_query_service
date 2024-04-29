from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from main.models import Query
from main.paginators import CustomPagination
from main.serializers import QuerySerializer

from main.tasks import simulating_server_response


class QueryCreateAPIView(generics.CreateAPIView):
    """
    Создание запроса по кадастровому номеру
    """
    queryset = Query.objects.all()
    serializer_class = QuerySerializer

    def create(self, request, *args, **kwargs) -> Response:
        """
        Метод создает запрос по кадастровому
        номеру, ширине и долготе.
        Записывает в базу данных.
        Эмулирует ответ сервера.
        """

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # Сохраняем данные запроса в БД
            self.perform_create(serializer)

            # Получаем кадастровый номер
            number = serializer.instance.number
            # Получаем id
            id_query = serializer.instance.id

            # Вызываем асинхронную задачу
            simulating_server_response.delay(id_query)

            return Response(
                {
                    "message": "Запрос по кадастровому номеру: "
                               f"{number} отправлен. "
                               f"id запроса: {id_query}. "
                               "Ожидайте ответ сервера."},
                status=status.HTTP_201_CREATED)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)


class QueryResultAPIView(generics.GenericAPIView):
    """
    Получение результата запроса
    из поля 'server_response' объекта
    Query по id.
    """
    queryset = Query.objects.all()
    serializer_class = QuerySerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='id запроса',
                required=True
            )
        ]
    )
    def get(self, request, *args, **kwargs) -> Response:
        """
        Метод получает id запроса.
        Возвращает результат запроса.
        """
        id_query = request.query_params.get('id')

        try:
            query_obj = self.queryset.get(id=id_query)

            if query_obj:

                result = query_obj.server_response

                if result is True:
                    return Response(
                        {"message": "Статус запроса: успешно"},
                        status=status.HTTP_200_OK)
                elif result is None:
                    return Response(
                        {
                            "message": "Статус запроса: "
                                       "ожидает ответ сервера"
                        },
                        status=status.HTTP_200_OK)
                else:
                    return Response(
                        {
                            "message": "Статус запроса: "
                                       "неуспешно"
                        },
                        status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response(
                {
                    "message": "Запроса с данным "
                               "id не существует "
                               "или вы передали пустой запрос."
                },
                status=status.HTTP_400_BAD_REQUEST)

        except ValueError:
            return Response(
                {
                    "message": "Вы передали пустой"
                               " запрос или некорректный id."
                },
                status=status.HTTP_400_BAD_REQUEST)


class QueryListAPIView(generics.ListAPIView):
    """
    Список всех запросов
    """
    queryset = Query.objects.all().order_by('id')
    serializer_class = QuerySerializer
    pagination_class = CustomPagination


class QueryNumberListAPIView(generics.ListAPIView):
    """
    Список запросов по кадастровому номеру
    """
    queryset = Query.objects.all().order_by('id')
    serializer_class = QuerySerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='number',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='кадастровый номер запроса',
                required=True
            )
        ]
    )
    def get(self, request, *args, **kwargs) -> Response:
        """
        Метод получает кадастровый номер.
        Возвращает отфильтрованные объекты
        Query по данному номеру.
        """
        number = request.query_params.get('number')

        # получаем все объекты по номеру
        querys = self.queryset.filter(number=number).all()

        # сериализуем объекты
        serializer = self.serializer_class(querys, many=True)

        if querys:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "message": "По данному кадастровому "
                               "номеру запросы не найдены"
                },
                status=status.HTTP_200_OK)


class PingAPIView(generics.GenericAPIView):
    """
    Проверка доступности сервера.
    """

    @swagger_auto_schema(
        responses={200: openapi.Response(description="Сервер доступен")},
    )
    def get(self, request, *args, **kwargs) -> Response:
        """
        Метод проверяет доступность сервера.
        Возвращает сообщение о доступности.
        """

        return Response(
            {"message": "Сервер доступен"},
            status=status.HTTP_200_OK)
