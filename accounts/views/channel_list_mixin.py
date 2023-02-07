from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.utils.module_loading import import_string
from django.views.generic.list import ListView

from accounts.models import Channel


class ChannelListMixin(LoginRequiredMixin):
    template_name = "accounts/channel_list.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        channels = [
            channel.get_typed_instance()
            for channel in Channel.objects.filter(site=self.request.site)
        ]
        context_data.update(
            {
                "object_list": channels,
                "channel_forms": {
                    channel.content_type: import_string(channel.CONFIG_FORM)(
                        instance=channel,
                        auto_id="id_%%s_%d" % channel.pk,
                        site=self.request.site,
                    )
                    for channel in channels
                },
                "new_channel_forms": {
                    ContentType.objects.get_for_model(model): import_string(
                        model.CONFIG_FORM
                    )(site=self.request.site)
                    for model in apps.get_app_config("accounts").get_models()
                    if issubclass(model, Channel) and model is not Channel
                },
            }
        )

        return context_data
