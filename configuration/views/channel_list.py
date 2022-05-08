from django.views.generic.list import ListView
from configuration.models import Channel
from .current_account_mixin import CurrentAccountMixin
from configuration.forms import channel_form_classes
from django.contrib.contenttypes.models import ContentType


class ChannelList(CurrentAccountMixin, ListView):
    model = Channel

    def get_queryset(self):
        return super().get_queryset()#.filter(account=self.current_account)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data.update({
            'new_channel_forms': { 
                content_type : channel_form_classes[model_class](account=self.current_account) 
                    for model_class , content_type in ContentType.objects.get_for_models(*channel_form_classes.keys()).items() 
            },
            'channel_forms': [channel_form_classes[type(channel.get_typed_instance())](
                    instance=channel.get_typed_instance(), 
                    auto_id='id_%%s_%d' % channel.pk,
                    account=self.current_account
                ) for channel in self.get_queryset()]
        })

        return context_data