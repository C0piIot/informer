from django.views.generic.list import ListView
from configuration.models import Environment
from configuration.forms import NewEnvironmentForm

class EnvironmentList(ListView):
	model = Environment

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data.update({
			'new_environment_form' : NewEnvironmentForm()
		})
		return context_data
