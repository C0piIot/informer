from .new_environment_form import NewEnvironmentForm
from .email_channel_form import EmailChannelForm
from .email_contact_form import EmailContactForm
from configuration.models import *

channel_form_classes = { 
    form_class.Meta.model : form_class for form_class in [
        EmailChannelForm, 
    ]
}

contact_form_classes = {
    
}