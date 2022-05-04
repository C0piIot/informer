from django import forms
from configuration.models import EmailChannel
from django.utils.translation import gettext_lazy as _

class EmailChannelForm(forms.ModelForm):

    account = None

    def __init__(self, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(**kwargs)

    def save(self):
        email_channel = super().save(commit=False)
        email_channel.account = self.account
        email_channel.save()
        return email_channel


    class Meta:
        model = EmailChannel
        fields = ('name', 'enabled', 'host', 'port', 'username', 'password')
