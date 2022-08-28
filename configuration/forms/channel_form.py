from django import forms

class ChannelForm(forms.ModelForm):

    account = None

    def __init__(self, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(**kwargs)

    def save(self):
        channel = super().save(commit=False)
        channel.account = self.account
        channel.save()
        return channel

