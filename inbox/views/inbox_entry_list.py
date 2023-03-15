from django.conf import settings
from django.utils.module_loading import import_string
from django.views.generic.detail import DetailView

from accounts.views import CurrentEnvironmentMixin
from contacts.models import Contact

inbox_storage = import_string(settings.INBOX_ENTRY_STORAGE)
contact_storage = import_string(settings.CONTACT_STORAGE)


class InboxEntryList(CurrentEnvironmentMixin, DetailView):
    model = Contact
    template_name = "inbox/inbox_entry_list.html"

    def get_object(self):
        return contact_storage.get_contact(
            self.current_environment, self.kwargs["key"])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        inbox_entries, cursor = inbox_storage.get_entries(
            self.current_environment,
            context_data["object"],
            cursor=self.request.GET.get("cursor", None),
            amount=50,
        )
        context_data["object_list"] = inbox_entries
        return context_data
