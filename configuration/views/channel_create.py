from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .current_account_mixin import CurrentAccountMixin
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from configuration.forms import channel_form_classes
from django.contrib.contenttypes.models import ContentType

class ChannelCreate(CurrentAccountMixin, SuccessMessageMixin, CreateView):
    success_url = reverse_lazy('configuration:channel_list')
    success_message = _("%(name)s was created successfully")

    def get_form_class(self):
        try:
            content_type = ContentType.objects.get_by_natural_key('configuration', self.kwargs['type'])
            return channel_form_classes[content_type.model_class()]
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
