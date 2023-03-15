from django.urls import path

from .views import *

app_name = "stats"

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
]
