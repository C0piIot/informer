from django import forms
from configuration.models import Environment
from django.utils.translation import gettext_lazy as _

class NewEnvironmentForm(forms.ModelForm):

    source_environment = forms.ModelChoiceField(
        queryset=Environment.objects.all(),
        required=False,
        label=_('Copy from'),
        help_text=_('Copy pipelines from existing environment')
    )

    class Meta:
        model = Environment
        fields = ['name']