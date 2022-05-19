from django.views.generic.list import ListView
from configuration.models import Channel
from .current_account_mixin import CurrentAccountMixin
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils.module_loading import import_string

class ChannelList(CurrentAccountMixin, ListView):
    model = Channel

    def get_queryset(self):
        return super().get_queryset()#.filter(account=self.current_account)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'new_channel_forms': { 
                ContentType.objects.get_by_natural_key('configuration', model) :  import_string(form_class)(account=self.current_account) 
                    for model, form_class in settings.CHANNEL_CONFIG_FORMS.items()
            },
            'channel_forms': [
                import_string(
                    settings.CHANNEL_CONFIG_FORMS[
                        ContentType.objects.get_for_model(channel.get_typed_instance()).model
                    ])(
                        instance=channel.get_typed_instance(),
                        auto_id='id_%%s_%d' % channel.pk,
                        account=self.current_account
                    )
                for channel in self.get_queryset()
            ] 
        })

        return context_data