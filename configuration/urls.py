from .views import *
from django.urls import path, include

app_name = 'configuration'

urlpatterns = [
    path('environments/', include([
        path('', EnvironmentList.as_view(), name='environment_list'),
        path('new/', EnvironmentCreate.as_view(), name='environment_new'),
        path('<slug:slug>/remove/', EnvironmentRemove.as_view(), name='environment_remove'),
    ])),
    path('channels/', include([
        path('', ChannelList.as_view(), name='channel_list'),
        #path('new/', EnvironmentCreate.as_view(), name='environment_new'),
        #path('<slug:slug>/remove/', EnvironmentRemove.as_view(), name='environment_remove'),
    ])),
]
