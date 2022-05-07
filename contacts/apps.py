from django.apps import AppConfig


class ContactsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contacts'
    DEFAULT_SETTINGS = {
        'CONTACT_STORAGE': 'contacts.models.Contact',
    }


    def ready(self):
        from django.conf import settings
        for name, value in self.DEFAULT_SETTINGS.items():
            if not hasattr(settings, name):
                setattr(settings, name, value)