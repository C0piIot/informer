from django.views.generic.list import ListView
from configuration.models import Channel
from .current_account_mixin import CurrentAccountMixin

class ChannelList(CurrentAccountMixin, ListView):
    model = Channel

    def get_queryset(self, **kwargs):
        return super().get_queryset(**kwargs).filter(account=self.current_account)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            #'new_environment_form' : NewEnvironmentForm(account=self.current_account)
        })
        return context_data