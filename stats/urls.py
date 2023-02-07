from django.urls import include, path

from .storages import BaseSeriesStorage
from .views import *

app_name = "stats"

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
]
