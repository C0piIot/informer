from django.views.generic.base import TemplateView, RedirectView
from django.urls import reverse
from configuration.models import Environment

class HomeRedirect(RedirectView):
	 def get_redirect_url(self, *args, **kwargs):
	 	if environment := Environment.objects.first():
	 		return reverse('pipelines:list', kwargs={'environment' : environment.slug })
	 	else:
	 		return reverse('configuration:environment_list')