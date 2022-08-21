from django.forms import ModelForm
from pipelines.models import Pipeline

class PipelineForm(ModelForm):
    class Meta:
        model = Pipeline
        fields = ('name', 'trigger', 'enabled',)