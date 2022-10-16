from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .current_account_mixin import CurrentAccountMixin
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.module_loading import import_string
from django.http import Http404
from django.conf import settings

class ChannelCreate(CurrentAccountMixin, SuccessMessageMixin, CreateView):
    success_url = reverse_lazy('accounts:channel_list')
    success_message = _("Channel was created successfully")

    def get_form_class(self):
        try:
            return import_string(
                settings.CHANNEL_CONFIG_FORMS[
                    ContentType.objects.get_by_natural_key(
                        'configuration',
                        self.kwargs['type']
                    ).model
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
        messages.error(self.request, _("Error creating channel"))
        return HttpResponseRedirect(self.success_url)
