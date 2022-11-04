from accounts.models import Environment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404


class CurrentEnvironmentMixin(LoginRequiredMixin):
	current_environment = None

	def setup(self, request, *args, **kwargs):
		super().setup(request, *args, **kwargs)
		self.current_environment = get_object_or_404(Environment, slug=kwargs.pop('environment'), site=self.request.site)
		

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data.update({ 'current_environment' : self.current_environment })
		return context_data


