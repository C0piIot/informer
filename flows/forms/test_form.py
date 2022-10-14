from django.forms import ModelForm
from flows.models import FlowRun

class TestForm(ModelForm):


    class Meta:
        model = FlowRun
        fields = ('contact_key', 'event_payload',)
