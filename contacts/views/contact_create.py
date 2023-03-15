from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView

from accounts.views import CurrentEnvironmentMixin
from contacts.forms import ContactForm
from contacts.models import Contact


class ContactCreate(CurrentEnvironmentMixin, SuccessMessageMixin, CreateView):
    form_class = ContactForm
    model = Contact
    success_message = _("%(name)s was created successfully")

    def get_success_url(self):
        return reverse(
            "contacts:list",
            kwargs={"environment": self.current_environment.slug})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"environment": self.current_environment})
        return kwargs
