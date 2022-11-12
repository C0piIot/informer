from  django.views.generic.base import TemplateView
from django.utils.module_loading import import_string
from django.conf import settings
from accounts.views import CurrentEnvironmentMixin

class ContactList(CurrentEnvironmentMixin, TemplateView):
	amount = 10
	template_name = 'contacts/contact_list.html'

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data.update({
			'object_list': import_string(settings.CONTACT_STORAGE).get_contacts(
				self.current_environment,
				amount=self.amount,
				start_key=self.request.GET.get('start_key', None)
			),
			'amount' : self.amount
		})
		return context_data