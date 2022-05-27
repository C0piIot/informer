from django.views.generic.edit import CreateView
from contacts.forms import ContactForm
from configuration.views import CurrentEnvironmentMixin
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


class ContactCreate(CurrentEnvironmentMixin, SuccessMessageMixin, CreateView):
    form_class = ContactForm
    success_message = _("%(name)s was created successfully")

    def get_success_url(self):
        return reverse('contacts:list', kwargs={'environment': self.current_environment.slug})

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'environment': self.current_environment
        })
        return kwargs

    def form_invalid(self, form, **kwargs):
        messages.error(self.request, _("Error creating contact"))
        return HttpResponseRedirect(self.get_success_url())