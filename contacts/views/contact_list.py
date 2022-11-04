from  django.views.generic.base import TemplateView
from django.utils.module_loading import import_string
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin


class ContactList(LoginRequiredMixin, TemplateView):

	template_name = 'contacts/contact_list.html'

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data.update({
			'object_list': import_string(settings.CONTACT_STORAGE).get_contacts(self.current_environment),
		})
		return context_data