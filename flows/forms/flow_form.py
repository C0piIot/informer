from django.forms import ModelForm
from flows.models import Flow

class FlowForm(ModelForm):
    class Meta:
        model = Flow
        fields = ('name', 'trigger', 'enabled', 'preview_context')
