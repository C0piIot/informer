from .views import *
from .views.steps import *
from django.urls import path, include

app_name = 'pipelines'

urlpatterns = [
    path('<slug:environment>/', include([
        path('', PipelineList.as_view(), name='home'),
        path('new/', PipelineCreate.as_view(), name='new'),
        path('<uuid:id>/history/', PipelineHistory.as_view(), name='history'),
        path('<uuid:id>/edit/', PipelineEdit.as_view(), name='edit'),
        path('<uuid:id>/remove/', PipelineRemove.as_view(), name='remove'),
        path('<uuid:id>/<int:pk>/remove', StepRemove.as_view(), name='step_remove'),
        path('<uuid:id>/delay/new', DelayCreate.as_view(), name='delay_new'),
        path('<uuid:id>/group/new', GroupCreate.as_view(), name='group_new'),
    ]))
]
