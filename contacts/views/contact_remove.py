from django.views.generic.edit import DeleteView
from contacts.forms import ContactForm
from configuration.views import CurrentEnvironmentMixin
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib import messages
from django.utils.module_loading import import_string
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings

class ContactRemove(CurrentEnvironmentMixin, SuccessMessageMixin, DeleteView):
    success_message = _("Contact was removed successfully")

    def get_object(self):
        return import_string(settings.CONTACT_STORAGE).get_model(self.current_environment, self.kwargs['key'])

    def get_success_url(self):
        return reverse('contacts:list', kwargs={'environment': self.current_environment.slug})

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())
