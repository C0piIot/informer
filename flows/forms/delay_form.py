from django.forms import ModelForm
from flows.models import Delay


class DelayForm(ModelForm):
    class Meta:
        model = Delay
        fields = ("time",)
