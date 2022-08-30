from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re

class FCMTokensWidget(forms.Textarea):

    def __init__(self, attrs=None):
        default_attrs = {"spellcheck": "false"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def format_value(self, value):
        if value is None:
            return None
        return "\n".join(value)


class FCMTokensField(forms.Field):
    widget = FCMTokensWidget
    validation = re.compile("^[0-9A-Za-z_:-]{100,500}$")

    def to_python(self, value):
        lines = [s.strip() for s in value.splitlines()]
        for line in lines:
            if not self.validation.match(line):
                raise ValidationError(_('Invalid tokens'))
        return lines


class PushContactForm(forms.Form):
    fcm_tokens = FCMTokensField(label=_('FCM Tokens'), required=False, help_text=_('Enter one registration token per line'))
