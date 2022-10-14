from accounts.models import Environment
from .current_account_mixin import CurrentAccountMixin
from django.shortcuts import get_object_or_404


class CurrentEnvironmentMixin(CurrentAccountMixin):
	current_environment = None

	def setup(self, request, *args, **kwargs):
		super().setup(request, *args, **kwargs)
		self.current_environment = get_object_or_404(Environment, slug=kwargs.pop('environment'), account=self.current_account)
		

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data.update({ 'current_environment' : self.current_environment })
		return context_data


