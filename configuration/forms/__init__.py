from .new_environment_form import NewEnvironmentForm
from .email_channel_form import EmailChannelForm
from .email_contact_form import EmailContactForm
from configuration.models import *
from django.utils.module_loading import import_string
from django.conf import settings

def get_contact_form(model):
    return import_string(settings.CHANNEL_CONTACT_FORMS[model])
