from django.views.generic.edit import CreateView
from contacts.forms import ContactForm
from configuration.views import CurrentEnvironmentMixin
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _


class ContactCreate(CurrentEnvironmentMixin, CreateView):
    form_class = ContactForm

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, **kwargs):
        messages.error(self.request, _("Error creating channel"))
        return HttpResponseRedirect(self.success_url)