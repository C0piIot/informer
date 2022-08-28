from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .current_account_mixin import CurrentAccountMixin
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.utils.module_loading import import_string
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.http import Http404
from configuration.models import Channel


class ChannelUpdate(CurrentAccountMixin, SuccessMessageMixin, UpdateView):
    success_url = reverse_lazy('configuration:channel_list')
    success_message = _("Channel was updated successfully")
    model = Channel

    def get_queryset(self):
        return super().get_queryset().filter(account=self.current_account)

    def get_object(self):
        return super().get_object().get_typed_instance()

    def get_form_class(self):
        try:
            return import_string(
                settings.CHANNEL_CONFIG_FORMS[
                    ContentType.objects.get_for_model(self.get_object()).model
                ]
            )
        except (ContentType.DoesNotExist, KeyError):
            raise Http404
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'account' : self.current_account})
        return kwargs

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form, **kwargs):
        messages.error(self.request, _("Error updating channel"))
        return HttpResponseRedirect(self.success_url)
