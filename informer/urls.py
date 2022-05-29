from django.contrib import admin
from django.urls import path, include
from .views import HomeRedirect

urlpatterns = [
    path('', HomeRedirect.as_view(), name='home'),
    path('pipelines/', include('pipelines.urls')),
    path('config/', include('configuration.urls')),
    path('admin/', admin.site.urls),
    path('contacts/', include('contacts.urls')),
    path('api-auth/', include('rest_framework.urls'))
]
