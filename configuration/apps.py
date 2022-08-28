from django.apps import AppConfig


class ConfigurationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'configuration'
    DEFAULT_SETTINGS = {
        'CHANNEL_CONTACT_FORMS' : {
            'emailchannel': 'configuration.forms.EmailContactForm',
            'pushchannel': 'configuration.forms.PushContactForm'
        },
        'CHANNEL_CONFIG_FORMS' : {
            'emailchannel': 'configuration.forms.EmailChannelForm',
            'pushchannel': 'configuration.forms.PushChannelForm'
        }   
    }

    def ready(self):
        from django.conf import settings
        for name, value in self.DEFAULT_SETTINGS.items():
            if not hasattr(settings, name):
                setattr(settings, name, value)
