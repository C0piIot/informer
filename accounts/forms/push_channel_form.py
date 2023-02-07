from django import forms
from django.utils.translation import gettext_lazy as _

from accounts.models import PushChannel

from .channel_form import ChannelForm


class PushChannelForm(ChannelForm):
    class Meta:
        model = PushChannel
        fields = (
            "enabled",
            "firebase_credentials",
        )
