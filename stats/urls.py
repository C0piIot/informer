from django.urls import include, path

from .views import *

app_name = "stats"

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
]
