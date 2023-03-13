from flows.models import *

from .delay_form import DelayForm
from .do_not_disturb_form import DoNotDisturbForm
from .email_form import EmailForm
from .flow_form import FlowForm
from .group_form import GroupForm
from .push_form import PushForm
from .test_form import TestForm
from .webhook_form import WebhookForm

step_form_classes = {
    form_class.Meta.model: form_class
    for form_class in [
        DelayForm,
        DoNotDisturbForm,
        GroupForm,
        EmailForm,
        PushForm,
        WebhookForm,
    ]
}
