from .delay_form import DelayForm
from .group_form import GroupForm
from .email_form import EmailForm
from .pipeline_form import PipelineForm
from pipelines.models import *

step_form_classes = { 
    form_class.Meta.model : form_class for form_class in [
        DelayForm, 
        GroupForm, 
        EmailForm 
    ]
}