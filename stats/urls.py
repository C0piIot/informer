from .views import *
from django.urls import path, include
from .storages import BaseSeriesStorage

app_name = 'stats'

urlpatterns = [
	path('', Dashboard.as_view(), name='dashboard'),
]