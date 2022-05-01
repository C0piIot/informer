from django import forms
from configuration.models import Environment
from django.utils.translation import gettext_lazy as _
from django.db import transaction

class NewEnvironmentForm(forms.ModelForm):

    account = None

    source_environment = forms.ModelChoiceField(
        queryset=Environment.objects.all(),
        required=False,
        label=_('Copy from'),
        help_text=_('Copy pipelines from existing environment')
    )

    def __init__(self, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(**kwargs)
        self.fields['source_environment'].queryset = self.fields['source_environment'].queryset.filter(account=self.account)

    def save(self):
        with transaction.atomic():
            environment = super().save(commit=False)
            environment.account = self.account
            environment.save()
            if self.cleaned_data['source_environment']:
                environment.pipelines.add(*self.cleaned_data['source_environment'].pipelines.all())
        return environment


    class Meta:
        model = Environment
        fields = ['name']


