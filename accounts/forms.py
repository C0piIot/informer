import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from accounts.models import EmailChannel, Environment, PushChannel


class ChannelForm(forms.ModelForm):
    def __init__(self, **kwargs):
        site = kwargs.pop("site")
        super().__init__(**kwargs)
        self.instance.site = site


class EmailChannelForm(ChannelForm):
    class Meta:
        model = EmailChannel
        fields = (
            "enabled",
            "host",
            "port",
            "security",
            "username",
            "password",
            "from_email",
        )
        widgets = {"password": forms.PasswordInput(render_value=True)}


class EmailContactForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        help_text=_(
            "Flow steps using the channel email will deliver "
            "emails to this address"
        ),
    )


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label=_("Email"))


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


class PushChannelForm(ChannelForm):
    class Meta:
        model = PushChannel
        fields = (
            "enabled",
            "firebase_credentials",
        )


class TokensWidget(forms.Textarea):
    def __init__(self, attrs=None):
        default_attrs = {"spellcheck": "false"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def format_value(self, value):
        if value is None:
            return None
        return "\n".join(value) if isinstance(value, list) else value


fcm_token_validation = re.compile("^[0-9A-Za-z_:-]{100,500}$")
apns_token_validation = re.compile("^[0-9a-fA-F]{1,500}$")


class MultipleTokensField(forms.Field):
    widget = TokensWidget
    help_text = _("Enter one registration token per line")

    def __init__(self, *args, **kwargs):
        self.token_validation = kwargs.pop("token_validation")
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        lines = [s.strip() for s in value.splitlines()] if value else []
        for line in lines:
            if not self.token_validation.match(line):
                raise ValidationError(_("Invalid tokens"))
        return lines


class PushContactForm(forms.Form):
    fcm_tokens = MultipleTokensField(
        label=_("FCM Tokens"),
        required=False, token_validation=fcm_token_validation)
    apns_tokens = MultipleTokensField(
        label=_("APNS Tokens"),
        required=False, token_validation=apns_token_validation)
