from  django.views.generic.base import TemplateView
from django.utils.module_loading import import_string
from django.conf import settings
from accounts.views import CurrentEnvironmentMixin
from contacts.forms import ContactForm


class ContactList(CurrentEnvironmentMixin, TemplateView):

	template_name = 'contacts/contact_list.html'

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		contacts = import_string(settings.CONTACT_STORAGE).get_contacts(self.current_environment)
		
		context_data.update({
			'object_list': contacts,
			'form': ContactForm(environment=self.current_environment),
			'contact_forms': (ContactForm(environment=self.current_environment, instance=contact)
				for contact in contacts
				)
		})
		return context_data