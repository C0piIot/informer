from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import UpdateView

from accounts.models import Channel

from .channel_list_mixin import ChannelListMixin


class ChannelUpdate(ChannelListMixin, SuccessMessageMixin, UpdateView):
    success_url = reverse_lazy("accounts:channel_list")
    success_message = _("Channel was updated successfully")
    model = Channel
    type = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        try:
            self.type = ContentType.objects.get_for_model(
                self.get_object().get_typed_instance()
            )
        except (ContentType.DoesNotExist, KeyError):
            raise Http404

    def get_queryset(self):
        return super().get_queryset().filter(site=self.request.site)

    def get_form_class(self):
        return import_string(self.type.model_class().CONFIG_FORM)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = kwargs["instance"].get_typed_instance()
        kwargs.update(site=self.request.site)
        return kwargs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["channel_forms"].update({self.type: context_data["form"]})
        return context_data
