from .views import *
from django.urls import path, include

app_name = 'contacts'

urlpatterns = [
    path('<slug:environment>/', include([
        path('', ContactList.as_view(), name='contact_list'),
    ]))
]
