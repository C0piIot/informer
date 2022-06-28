from .views import *
from .views.steps import *
from .models import *
from .forms import *
from django.urls import path, include
from rest_framework import routers
from rest_framework.schemas import get_schema_view


app_name = 'pipelines'

router = routers.SimpleRouter()
router.register(r'', EventListener, basename='event')

urlpatterns = [
    
    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'), 
    path('', include(router.urls)),
    path('', PipelineList.as_view(), name='list'),
    path('create/', PipelineCreate.as_view(), name='create'),
    path('<uuid:id>/', PipelineHistory.as_view(), name='history'),
    path('<uuid:id>/<uuid:revision>/', PipelineHistory.as_view(), name='history'),
    path('<uuid:id>/edit/', PipelineEdit.as_view(), name='edit'),
    path('<uuid:id>/remove/', PipelineRemove.as_view(), name='remove'),
    path('<uuid:id>/<int:pk>/', StepEdit.as_view(), name='step_edit'),
    path('<uuid:id>/<int:pk>/move/', StepMove.as_view(), name='step_move'),
    path('<uuid:id>/<int:pk>/remove/', StepRemove.as_view(), name='step_remove'),
    path('<uuid:id>/<slug:type>/create/', StepCreate.as_view(), name='step_create'),
    path('<uuid:id>/runs/', PipelineRunList.as_view(), name='runs'),
    path('<uuid:id>/runs/<uuid:pipeline_run_id>/', PipelineRunDetail.as_view(), name='run'),  
    path('render_mail/', RenderMail.as_view(), name='render_mail'),
]
