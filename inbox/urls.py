from .views import *
from django.urls import path, include
from informer.api import router
from contacts.views import ContactList
from inbox.views import InboxEntryList

app_name = 'inbox'

router.register('inbox', InboxEntryViewSet)

urlpatterns = [
	path('', ContactList.as_view(template_name='inbox/inbox_list.html'), name='list'),
	path('<slug:key>/', InboxEntryList.as_view(), name='inbox_entry_list'),
]
