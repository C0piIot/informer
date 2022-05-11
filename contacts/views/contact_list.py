from  django.views.generic.base import TemplateView
from django.utils.module_loading import import_string
from django.conf import settings
from configuration.views import CurrentEnvironmentMixin


class ContactList(CurrentEnvironmentMixin, TemplateView):

	template_name = 'contacts/contact_list.html'

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		contact_storage = import_string(settings.CONTACT_STORAGE)
		context_data.update({
			'contacts': contact_storage.get_contacts(self.current_environment, 0)
		})
		return context_data