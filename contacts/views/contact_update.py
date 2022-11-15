from django.views.generic.edit import UpdateView
from contacts.forms import ContactForm
from accounts.views import CurrentEnvironmentMixin
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.module_loading import import_string
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from contacts.models import Contact

class ContactUpdate(CurrentEnvironmentMixin, SuccessMessageMixin, UpdateView):
    form_class = ContactForm
    model = Contact
    success_message = _("%(name)s was updated successfully")


    def get_object(self):
        return import_string(settings.CONTACT_STORAGE).get_contact(self.current_environment, self.kwargs['key'])

    def get_success_url(self):
        return reverse('contacts:list', kwargs={'environment': self.current_environment.slug})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'environment': self.current_environment
        })
        return kwargs
