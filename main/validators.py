from rest_framework import serializers
import re


class CadastreNumberValidator:
    """
    Валидация кадастрового номера.
    """

    def __init__(self, field):
        self.field = field
        self.correct = r'^\d+:\d+:\d+:\d+$'

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)

        if not re.match(self.correct, tmp_val):
            raise serializers.ValidationError(
                'Неверный формат кадастрового номера.\n'
                'Введите номер в формате: АА:ВВ:CCCCСCC:КК, \n'
                'где:\n'
                'АА – кадастровый округ;\n'
                'ВВ - кадастровый район;\n'
                'CCCCCCС - кадастровый квартал в пределах '
                'данного кадастрового района  (состоит из 7 цифр);\n'
                'КК – уникальный номер объекта.'
            )


class LatitudeValidator:
    """
    Валидация широты.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)

        if not -90 <= tmp_val <= 90:
            raise serializers.ValidationError(
                'Неверный формат широты.\n'
                'Введите широту в диапазоне от -90 до 90.'
            )


class LongitudeValidator:
    """
    Валидация долготы.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)

        if not -180 <= tmp_val <= 180:
            raise serializers.ValidationError(
                'Неверный формат долготы.\n'
                'Введите долготу в диапазоне от -180 до 180.'
            )
