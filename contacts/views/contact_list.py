from django.views.generic.base import TemplateView
from django.utils.module_loading import import_string
from django.conf import settings
from accounts.views import CurrentEnvironmentMixin
from contacts.forms import ContactSearchForm

class ContactList(CurrentEnvironmentMixin, TemplateView):
	amount = 10
	template_name = 'contacts/contact_list.html'

	def get_context_data(self, **kwargs):
		context_data = super().get_context_data(**kwargs)
		context_data.update({
			'object_list': import_string(settings.CONTACT_STORAGE).get_contacts(
				self.current_environment,
				start_key=self.request.GET.get('start_key', None),
				filter_key=self.request.GET.get('filter_key', None),
				filter_name=self.request.GET.get('filter_name', None),
			),
			'amount' : self.amount,
			'form' : ContactSearchForm(self.request.GET),
			'next_url': None
		})
		if 0 < len(context_data['object_list']) >= self.amount:
			query = self.request.GET.copy()
			query['start_key'] = context_data['object_list'][-1].key
			context_data['next_url'] = '%s?%s' % (self.request.path, query.urlencode())

		return context_data