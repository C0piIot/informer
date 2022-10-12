from .views import *
from .views.steps import *
from .models import *
from .forms import *
from django.urls import path, include
from informer.api import router

app_name = 'pipelines'

router.register('pipeline-runs', PipelineRunViewSet)

urlpatterns = [
    path('', PipelineList.as_view(), name='list'),
    path('create/', PipelineCreate.as_view(), name='create'),
    path('<uuid:id>/', include([
        path('', PipelineHistory.as_view(), name='history'),
        path('<uuid:revision>/', PipelineHistory.as_view(), name='history'),
        path('edit/', PipelineEdit.as_view(), name='edit'),
        path('remove/', PipelineRemove.as_view(), name='remove'),
        path('set_revision/', PipelineSetRevision.as_view(), name='set_revision'),
        path('<int:pk>/', include([
            path('', StepEdit.as_view(), name='step_edit'),
            path('move/', StepMove.as_view(), name='step_move'),
            path('remove/', StepRemove.as_view(), name='step_remove'), 
        ])),
        path('<slug:type>/create/', StepCreate.as_view(), name='step_create'),
        path('runs/', include([
            path('', PipelineRunList.as_view(), name='runs'),
            path('<uuid:pipeline_run_id>/', PipelineRunDetail.as_view(), name='run'),  
        ]))
    ])),
    path('render_mail/', RenderMail.as_view(), name='render_mail'),
]
