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
                'Неверный формат кадастрового номера. '
                'Введите номер в формате: АА:ВВ:CCCCСCC:КК, '
                'где: '
                'АА – кадастровый округ; '
                'ВВ - кадастровый район; '
                'CCCCCCС - кадастровый квартал в пределах '
                'данного кадастрового района  (состоит из 7 цифр); '
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
                'Неверный формат широты. '
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
                'Неверный формат долготы. '
                'Введите долготу в диапазоне от -180 до 180.'
            )
