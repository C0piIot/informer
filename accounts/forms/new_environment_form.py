from django import forms
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from accounts.models import Environment


class NewEnvironmentForm(forms.ModelForm):

    class Meta:
        model = Environment
        fields = ["name"]
    source_environment = forms.ModelChoiceField(
        queryset=Environment.objects.all(),
        required=False,
        label=_("Copy from"),
        help_text=_("Copy flows from existing environment"),
    )

    def __init__(self, **kwargs):
        site = kwargs.pop("site")
        super().__init__(**kwargs)
        self.instance.site = site
        self.fields["source_environment"].queryset = self.fields[
            "source_environment"
        ].queryset.filter(site=site)

    def save(self):
        with transaction.atomic():
            environment = super().save()
            if self.cleaned_data["source_environment"]:
                environment.flows.add(
                    *self.cleaned_data["source_environment"].flows.all()
                )
        return environment
