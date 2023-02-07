from django import forms
from .channel_form import ChannelForm
from accounts.models import PushChannel
from django.utils.translation import gettext_lazy as _


class PushChannelForm(ChannelForm):
    class Meta:
        model = PushChannel
        fields = (
            "enabled",
            "firebase_credentials",
        )
