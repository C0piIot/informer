from .views import *
from .models import *
from django.urls import path, include
from django.views.generic.list import ListView

app_name = 'configuration'

urlpatterns = [
    path('environments/', ListView.as_view(model=Environment), name='environment_list'),
]
