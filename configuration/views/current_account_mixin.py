from configuration.models import Account
from django.shortcuts import get_object_or_404


class CurrentAccountMixin(object):
	current_environment = None

	def setup(self, request, *args, **kwargs):
		super().setup(request, *args, **kwargs)
		self.current_account = Account.objects.first()
		

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data.update({ 'current_account' : self.current_account })
		return context_data


