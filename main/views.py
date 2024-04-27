from rest_framework import generics, status
from rest_framework.response import Response

from main.models import Query
from main.serializers import QuerySerializer
from main.utils import random_response

from main.tasks import simulating_server_response


class QueryCreateAPIView(generics.CreateAPIView):
    """
    Создание запроса по кадастровому номеру
    """
    queryset = Query.objects.all()
    serializer_class = QuerySerializer

    def create(self, request, *args, **kwargs):
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
                f"Запрос по кадастровому номеру: {number} отправлен. "
                f"id запроса: {id_query}. "
                f"Ожидайте ответ сервера.",
                status=status.HTTP_201_CREATED)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)


class QueryListAPIView(generics.ListAPIView):
    """
    Список всех запросов
    """
    queryset = Query.objects.all()
    serializer_class = QuerySerializer


class QueryNumberListAPIView(generics.ListAPIView):
    """
    Список запросов по кадастровому номеру
    """
    queryset = Query.objects.all()
    serializer_class = QuerySerializer

    def get(self, request, *args, **kwargs):
        """
        Метод получает кадастровый номер.
        Возвращает отфильтрованные объекты
        Query по данному номеру.
        """
        numbers = request.data.get('number')
        querys = Query.objects.filter(number=numbers)

        if querys:
            return Response(querys, status=status.HTTP_200_OK)
        else:
            return Response(
                'По данному кадастровому номеру запросы не найдены',
                status=status.HTTP_200_OK)
