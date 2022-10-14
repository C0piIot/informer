from django.forms import ModelForm
from flows.models import FlowRun
from django.conf import settings
from django.utils.module_loading import import_string


class TestForm(ModelForm):

    flow = None
    environment = None

    def __init__(self, **kwargs):
        self.flow = kwargs.pop('flow')
        self.environment = kwargs.pop('environment')
        super().__init__(**kwargs)

    def save(self, commit=True):
        flow_run = super().save(commit=False)
        flow_run.flow_revision = self.flow
        if commit:
            import_string(settings.FLOW_RUN_STORAGE).save_flow_run(self.environment, flow_run)
        return flow_run
            
    class Meta:
        model = FlowRun
        fields = ('contact_key', 'event_payload',)
