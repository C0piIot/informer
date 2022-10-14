from .views import *
from .views.steps import *
from .models import *
from .forms import *
from django.urls import path, include
from informer.api import router

app_name = 'flows'

router.register('flow-runs', FlowRunViewSet)

urlpatterns = [
    path('', FlowList.as_view(), name='list'),
    path('create/', FlowCreate.as_view(), name='create'),
    path('<uuid:id>/', include([
        path('', FlowHistory.as_view(), name='history'),
        path('<uuid:revision>/', FlowHistory.as_view(), name='history'),
        path('edit/', FlowEdit.as_view(), name='edit'),
        path('test/', FlowTest.as_view(), name='test'),
        path('remove/', FlowRemove.as_view(), name='remove'),
        path('set_revision/', FlowSetRevision.as_view(), name='set_revision'),
        path('<int:pk>/', include([
            path('', StepEdit.as_view(), name='step_edit'),
            path('move/', StepMove.as_view(), name='step_move'),
            path('remove/', StepRemove.as_view(), name='step_remove'), 
        ])),
        path('<slug:type>/create/', StepCreate.as_view(), name='step_create'),
        path('runs/', include([
            path('', FlowRunList.as_view(), name='runs'),
            path('<uuid:flow_run_id>/', FlowRunDetail.as_view(), name='run'),  
        ]))
    ])),
    path('render_mail/', RenderMail.as_view(), name='render_mail'),
]
