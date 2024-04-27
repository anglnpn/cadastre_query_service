from rest_framework import generics

from main.models import Query
from main.serializers import QuerySerializer


class QueryCreateAPIView(generics.CreateAPIView):
    """
    Создание запроса по кадастровому номеру
    """
    queryset = Query.objects.all()
    serializer_class = QuerySerializer


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


