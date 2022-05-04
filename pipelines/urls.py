from .views import *
from .views.steps import *
from .models import *
from .forms import *
from django.urls import path, include

app_name = 'pipelines'

urlpatterns = [
    path('<slug:environment>/', include([
        path('', PipelineList.as_view(), name='list'),
        path('create/', PipelineCreate.as_view(), name='create'),
        path('<uuid:id>/history/', PipelineHistory.as_view(), name='history'),
        path('<uuid:id>/edit/', PipelineEdit.as_view(), name='edit'),
        path('<uuid:id>/remove/', PipelineRemove.as_view(), name='remove'),
        path('<uuid:id>/<int:pk>/remove/', StepRemove.as_view(), name='step_remove'),
        path('<uuid:id>/delay/create/', StepCreate.as_view(model=Delay, fields=('time',)), name='delay_create'),
        path('<uuid:id>/group/create/', StepCreate.as_view(model=Group, form_class=GroupForm), name='group_create'),
        path('<uuid:id>/email/create/', StepCreate.as_view(model=Email, form_class=EmailForm), name='email_create'),
    ]))
]
