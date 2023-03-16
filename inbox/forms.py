""" Inbox forms """
from django.forms import ModelForm

from inbox.models import Inbox


class InboxForm(ModelForm):
    class Meta:
        model = Inbox
        fields = (
            "title",
            "message",
            "url",
            "image",
            "entry_data",
        )
