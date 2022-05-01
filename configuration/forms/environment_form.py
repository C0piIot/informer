from django.forms import ModelForm
from configuration.models import Environment

class EnvironmentForm(ModelForm):
    class Meta:
        model = Environment
        fields = ['name']