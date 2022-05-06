from django.views.generic.list import ListView
from configuration.models import Channel
from .current_account_mixin import CurrentAccountMixin
from configuration.forms import EmailChannelForm
from django.contrib.contenttypes.models import ContentType


class ChannelList(CurrentAccountMixin, ListView):
    model = Channel

    form_classes = { 
        form_class.Meta.model : form_class for form_class in [
            EmailChannelForm, 
        ]
    }

    def get_queryset(self):
        return super().get_queryset()#.filter(account=self.current_account)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data.update({
            'new_channel_forms': { 
                content_type : self.form_classes[model_class](account=self.current_account) 
                    for model_class , content_type in ContentType.objects.get_for_models(*self.form_classes.keys()).items() 
            },
            'channel_forms': [self.form_classes[type(channel.get_typed_instance())](
                    instance=channel.get_typed_instance(), 
                    auto_id='id_%%s_%d' % channel.pk,
                    account=self.current_account
                ) for channel in self.get_queryset()]
        })

        return context_data