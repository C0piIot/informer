from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.http import HttpResponseRedirect
from accounts.models import Environment
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from .current_account_mixin import CurrentAccountMixin


class EnvironmentRemove(CurrentAccountMixin, SuccessMessageMixin, DeleteView):

    model = Environment
    success_url = reverse_lazy('accounts:environment_list')
    success_message = _("Environment was removed successfully")

    def get_queryset(self, **kwargs):
        return super().get_queryset(**kwargs).filter(account=self.current_account)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())
