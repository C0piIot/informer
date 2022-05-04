from django.forms import ModelForm
from pipelines.models import Delay

class DelayForm(ModelForm):
    class Meta:
        model = Delay
        fields = ('time',)