from django import forms
from django.utils.translation import gettext_lazy as _

from accounts.models import EmailChannel

from .channel_form import ChannelForm


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
