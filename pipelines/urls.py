from .views import *
from django.urls import path, include

app_name = 'pipelines'

urlpatterns = [
    path('<slug:environment>/', include([
        path('', PipelineList.as_view(), name='home'),
        path('new/', PipelineCreate.as_view(), name='new'),
        path('<uuid:pk>/edit/', PipelineEdit.as_view(), name='edit'),
        path('<uuid:pk>/remove/', PipelineRemove.as_view(), name='remove'),
    ]))
]
