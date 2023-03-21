from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from accounts.views import CurrentEnvironmentMixin
from contacts.forms import ContactForm, ContactSearchForm
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


class ContactList(CurrentEnvironmentMixin, TemplateView):
    amount = 10
    template_name = "contacts/contact_list.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {
                "amount": self.amount,
                "form": ContactSearchForm(self.request.GET),
                "next_url": None,
            }
        )
        context_data["object_list"], cursor = import_string(
            settings.CONTACT_STORAGE
        ).get_contacts(
            self.current_environment,
            cursor=self.request.GET.get("cursor", None),
            filter_key=self.request.GET.get("filter_key", None),
            filter_name=self.request.GET.get("filter_name", None),
        )

        if cursor:
            query = self.request.GET.copy()
            query["cursor"] = cursor
            context_data["next_url"] = f"{self.request.path}?{query.urlencode()}"

        return context_data


class ContactRemove(CurrentEnvironmentMixin, SuccessMessageMixin, DeleteView):
    success_message = _("Contact was removed successfully")

    def get_object(self):
        return import_string(settings.CONTACT_STORAGE).get_contact(
            self.current_environment, self.kwargs["key"]
        )

    def get_success_url(self):
        return reverse(
            "contacts:list",
            kwargs={"environment": self.current_environment.slug})

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())


class ContactUpdate(CurrentEnvironmentMixin, SuccessMessageMixin, UpdateView):
    form_class = ContactForm
    model = Contact
    success_message = _("%(name)s was updated successfully")

    def get_object(self):
        return import_string(settings.CONTACT_STORAGE).get_contact(
            self.current_environment, self.kwargs["key"]
        )

    def get_success_url(self):
        return reverse(
            "contacts:list",
            kwargs={"environment": self.current_environment.slug})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"environment": self.current_environment})
        return kwargs
