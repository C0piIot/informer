from .delay_form import DelayForm
from .group_form import GroupForm
from .email_form import EmailForm
from .push_form import PushForm
from .flow_form import FlowForm
from .test_form import TestForm
from .webhook_form import WebhookForm
from flows.models import *

step_form_classes = {
    form_class.Meta.model : form_class for form_class in [
        DelayForm,
        GroupForm,
        EmailForm,
        PushForm,
        WebhookForm
    ]
}
