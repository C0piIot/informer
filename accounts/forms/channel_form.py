from django import forms

class ChannelForm(forms.ModelForm):

    site = None

    def __init__(self, **kwargs):
        self.site = kwargs.pop('site')
        super().__init__(**kwargs)

    def save(self):
        channel = super().save(commit=False)
        channel.site = self.site
        channel.save()
        return channel

