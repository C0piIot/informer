from configuration.models import Environment
from django.shortcuts import get_object_or_404


class CurrentEnvironmentMixin(object):
	current_environment = None

	def setup(self, request, *args, **kwargs):
		super().setup(request, *args, **kwargs)
		if 'environment' in kwargs:
			self.current_environment = get_object_or_404(Environment, slug=kwargs['environment'])
		

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data.update({ 'current_environment' : self.current_environment })
		return context_data


