from  django.views.generic.base import TemplateView
from django.utils.module_loading import import_string
from django.conf import settings

class ContactList(TemplateView):

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)

		contact_storage = import_string(settings.CONTACT_STORAGE)
		

		print(contact_storage.get_contacts(0))
		
		return context_data