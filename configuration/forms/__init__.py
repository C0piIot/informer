from .new_environment_form import NewEnvironmentForm
from .email_channel_form import EmailChannelForm
from .push_channel_form import PushChannelForm
from .email_contact_form import EmailContactForm
from .push_contact_form import PushContactForm
from configuration.models import *
from django.utils.module_loading import import_string
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

def get_contact_form(model):
    return import_string(settings.CHANNEL_CONTACT_FORMS[ContentType.objects.get_for_model(model.get_typed_instance()).model])
