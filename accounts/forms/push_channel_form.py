
from accounts.models import PushChannel

from .channel_form import ChannelForm


class PushChannelForm(ChannelForm):
    class Meta:
        model = PushChannel
        fields = (
            "enabled",
            "firebase_credentials",
        )
