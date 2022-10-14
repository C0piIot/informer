from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .current_account_mixin import CurrentAccountMixin
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from accounts.models import Channel


class ChannelRemove(CurrentAccountMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy('configuration:channel_list')
    success_message = _("Channel was removed successfully")
    model = Channel

    def get_queryset(self):
        return super().get_queryset().filter(account=self.current_account)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)

