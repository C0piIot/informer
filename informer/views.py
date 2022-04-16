from django.views.generic.base import TemplateView, RedirectView
from django.urls import reverse
from configuration.models import Environment

class HomeRedirect(RedirectView):
	 def get_redirect_url(self, *args, **kwargs):
	 	return reverse('pipelines:home', kwargs={'environment' : Environment.objects.first().slug })