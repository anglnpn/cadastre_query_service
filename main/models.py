from django.db import models


class Query(models.Model):
    """
    Модель для сохранения данных
    запроса по кадастровому номеру
     в БД.
    """
    number = models.CharField(
        max_length=50,
        verbose_name='кадастровый номер')
    latitude = models.FloatField(
        verbose_name='широта')
    longitude = models.FloatField(
        verbose_name='долгота')
    date_query = models.DateField(
        auto_now=True,
        verbose_name='дата запроса')
    server_response = models.BooleanField(
        verbose_name='ответ сервера',
        null=True, blank=True)
