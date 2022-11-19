from django import forms

class ChannelForm(forms.ModelForm):

    def __init__(self, **kwargs):
        site = kwargs.pop('site')
        super().__init__(**kwargs)
        self.instance.site = site
