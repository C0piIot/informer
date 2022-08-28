from django import forms
from .channel_form import ChannelForm
from configuration.models import EmailChannel
from django.utils.translation import gettext_lazy as _

class EmailChannelForm(ChannelForm):

    class Meta:
        model = EmailChannel
        fields = ('enabled', 'host', 'port', 'security', 'username', 'password')
        widgets = { 'password' : forms.PasswordInput(render_value=True) }
