from .views import *
from django.urls import path, include
from informer.api import router

app_name = 'inbox'

router.register('inbox', InboxEntryViewSet)

urlpatterns = [
    
]
