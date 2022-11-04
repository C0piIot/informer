from django.views.generic.list import ListView
from accounts.models import Channel
from .current_site_mixin import CurrentSiteMixin
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils.module_loading import import_string

class ChannelListMixin(CurrentSiteMixin):
    template_name = 'accounts/channel_list.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        channels = Channel.objects.filter(site=self.request.site)
        context_data.update({
            'object_list': channels,
            'channel_forms': {
                channel.content_type : import_string(
                        settings.CHANNEL_CONFIG_FORMS[
                            ContentType.objects.get_for_model(channel.get_typed_instance()).model
                        ])(
                            instance=channel.get_typed_instance(),
                            auto_id='id_%%s_%d' % channel.pk,
                            site=self.request.site
                        )
                    for channel in channels
            },
            'new_channel_forms': { 
                ContentType.objects.get_by_natural_key('accounts', model) :  import_string(form_class)(site=self.request.site) 
                    for model, form_class in settings.CHANNEL_CONFIG_FORMS.items()
            },
        })

        return context_data