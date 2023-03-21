from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils.module_loading import import_string

from accounts.models import Channel, Environment


class CurrentEnvironmentMixin(LoginRequiredMixin):
    current_environment = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.current_environment = get_object_or_404(
            Environment, slug=kwargs.pop("environment"), site=self.request.site
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({"current_environment": self.current_environment})
        return context_data


class ContextAwareViewSetMixin(object):
    def initial(self, request, *args, **kwargs):
        self.current_environment = get_object_or_404(
            Environment, slug=kwargs.pop("environment"), site=self.request.site
        )
        super().initial(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"environment": self.current_environment})
        return context


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
                        auto_id=f"id_%s_{channel.pk}",
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
