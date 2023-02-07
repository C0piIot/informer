from django.forms import ModelForm
from flows.models import FlowRun
from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class TestForm(ModelForm):
    flow = None
    environment = None

    def __init__(self, **kwargs):
        self.flow = kwargs.pop("flow")
        self.environment = kwargs.pop("environment")
        super().__init__(**kwargs)

    def clean_contact_key(self):
        contact_key = self.cleaned_data["contact_key"]
        self.cleaned_data["contact"] = import_string(
            settings.CONTACT_STORAGE
        ).get_contact(self.environment, contact_key)
        if not self.cleaned_data["contact"]:
            raise ValidationError(
                _("Can't find contact with key %(contact_key)s"),
                code="invalid_contact_key",
                params={"contact_key": contact_key},
            )
        return contact_key

    def save(self, commit=True):
        flow_run = super().save(commit=False)
        flow_run.flow_revision = self.flow
        flow_run.contact = self.cleaned_data["contact"]
        if commit:
            import_string(settings.FLOW_RUN_STORAGE).save_flow_run(
                self.environment, flow_run
            )
            import_string(settings.FLOW_EXECUTOR).run(flow_run)
        return flow_run

    class Meta:
        model = FlowRun
        fields = (
            "contact_key",
            "event_payload",
        )
