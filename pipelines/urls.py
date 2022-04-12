from .views import *
from django.urls import path, include

app_name = 'pipelines'

urlpatterns = [
    path('', PipelineList.as_view(), name='home'),
    path('new/', PipelineCreate.as_view(), name='new'),
]
