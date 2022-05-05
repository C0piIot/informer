from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .current_account_mixin import CurrentAccountMixin
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from configuration.forms import EmailChannelForm

class ChannelCreate(CurrentAccountMixin, SuccessMessageMixin, CreateView):
    success_url = reverse_lazy('configuration:channel_list')
    success_message = _("%(name)s was created successfully")

    def get_queryset(self):
        return self.get_form_class().Meta.model

    def get_form_class(self):
        return EmailChannelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'account' : self.current_account})
        return kwargs

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, **kwargs):
        messages.error(self.request, _("Error creating channel"))
        return HttpResponseRedirect(self.success_url)
