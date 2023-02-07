from django.apps import AppConfig

#


class InboxConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "inbox"
    DEFAULT_SETTINGS = {
        "INBOX_ENTRY_STORAGE": "inbox.storages.DefaultInboxEntryStorage",
    }

    def ready(self):
        from django.conf import settings

        for name, value in self.DEFAULT_SETTINGS.items():
            if not hasattr(settings, name):
                setattr(settings, name, value)

        from flows.forms import step_form_classes

        from .forms import InboxForm

        step_form_classes[InboxForm.Meta.model] = InboxForm
