from django.urls import path

from main.apps import MainConfig
from main.views import (QueryCreateAPIView,
                        QueryListAPIView,
                        QueryNumberListAPIView,
                        QueryResultAPIView,
                        PingAPIView)

app_name = MainConfig.name

urlpatterns = [
    path('query/', QueryCreateAPIView.as_view(), name='query_create'),
    path('history/', QueryListAPIView.as_view(), name='history'),
    path('history_number/', QueryNumberListAPIView.as_view(), name='history_number'),
    path('result/', QueryResultAPIView.as_view(), name='history_result'),
    path('ping/', PingAPIView.as_view(), name='ping'),
]
