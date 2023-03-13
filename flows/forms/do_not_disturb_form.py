from django.forms import ModelForm

from flows.models import DoNotDisturb


class DoNotDisturbForm(ModelForm):
    class Meta:
        model = DoNotDisturb
        fields = (
            "start",
            "end",
        )
