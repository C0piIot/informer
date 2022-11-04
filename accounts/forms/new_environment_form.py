from django import forms
from accounts.models import Environment
from django.utils.translation import gettext_lazy as _
from django.db import transaction

class NewEnvironmentForm(forms.ModelForm):

    site = None

    source_environment = forms.ModelChoiceField(
        queryset=Environment.objects.all(),
        required=False,
        label=_('Copy from'),
        help_text=_('Copy flows from existing environment')
    )

    def __init__(self, **kwargs):
        self.site = kwargs.pop('site')
        super().__init__(**kwargs)
        self.fields['source_environment'].queryset = self.fields['source_environment'].queryset.filter(site=self.site)

    def save(self):
        with transaction.atomic():
            environment = super().save(commit=False)
            environment.site = self.site
            environment.save()
            if self.cleaned_data['source_environment']:
                environment.flows.add(*self.cleaned_data['source_environment'].flows.all())
        return environment


    class Meta:
        model = Environment
        fields = ['name']


