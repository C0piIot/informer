from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    DEFAULT_SETTINGS = {
        'CHANNEL_CONTACT_FORMS' : {
            'emailchannel': 'accounts.forms.EmailContactForm',
            'pushchannel': 'accounts.forms.PushContactForm'
        },
        'CHANNEL_CONFIG_FORMS' : {
            'emailchannel': 'accounts.forms.EmailChannelForm',
            'pushchannel': 'accounts.forms.PushChannelForm'
        }   
    }

    def ready(self):
        from django.conf import settings
        for name, value in self.DEFAULT_SETTINGS.items():
            if not hasattr(settings, name):
                setattr(settings, name, value)
