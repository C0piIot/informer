from django.conf import settings
from django.utils.module_loading import import_string
from django.views.generic.base import TemplateView

from accounts.views import CurrentEnvironmentMixin
from contacts.forms import ContactSearchForm


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
            context_data["next_url"] = "%s?%s" % (
                self.request.path, query.urlencode())

        return context_data
