from rest_framework import serializers

from main.models import Query
from main.validators import (CadastreNumberValidator,
                             LatitudeValidator,
                             LongitudeValidator)


class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = '__all__'
        validators = [
            CadastreNumberValidator('number'),
            LatitudeValidator('latitude'),
            LongitudeValidator('longitude')
        ]
