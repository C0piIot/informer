from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import DeleteView

from accounts.views import CurrentEnvironmentMixin
from contacts.forms import ContactForm


class ContactRemove(CurrentEnvironmentMixin, SuccessMessageMixin, DeleteView):
    success_message = _("Contact was removed successfully")

    def get_object(self):
        return import_string(settings.CONTACT_STORAGE).get_contact(
            self.current_environment, self.kwargs["key"]
        )

    def get_success_url(self):
        return reverse(
            "contacts:list", kwargs={"environment": self.current_environment.slug}
        )

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())
