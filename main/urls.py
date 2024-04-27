from django.urls import path

from main.apps import MainConfig
from main.views import QueryCreateAPIView, QueryListAPIView

app_name = MainConfig.name

urlpatterns = [
    path('query/', QueryCreateAPIView.as_view(), name='query_create'),
    path('history/', QueryListAPIView.as_view(), name='history'),
]

