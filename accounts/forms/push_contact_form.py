from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re


class TokensWidget(forms.Textarea):
    def __init__(self, attrs=None):
        default_attrs = {"spellcheck": "false"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def format_value(self, value):
        if value is None:
            return None
        return "\n".join(value) if type(value) == list else value


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
        label=_("FCM Tokens"), required=False, token_validation=fcm_token_validation
    )
    apns_tokens = MultipleTokensField(
        label=_("APNS Tokens"), required=False, token_validation=apns_token_validation
    )
