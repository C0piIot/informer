from .views import *
from django.urls import path, include
from informer.api import router

app_name = 'contacts'

router.register('contacts',ContactViewSet)

urlpatterns = [
    path('', ContactList.as_view(), name='list'),
    path('create/', ContactCreate.as_view(), name='contact_create'),
    path('<slug:key>/update/', ContactUpdate.as_view(), name='contact_update'),
    path('<slug:key>/remove/', ContactRemove.as_view(), name='contact_remove')
]
