from django import forms
from django.utils.translation import gettext_lazy as _
from contacts.models import Contact 
from configuration.models import Channel
from configuration.forms import get_contact_form

class ContactForm(forms.ModelForm):

    CHANNEL_PREFIX = 'channel-'
    environment = None
    channel_forms = None
    channels = forms.ModelMultipleChoiceField(
        required=False, 
        label=_('Channels'), 
        widget=forms.CheckboxSelectMultiple,
        queryset=Channel.objects.none()
    )

    def __init__(self, **kwargs):
        self.environment = kwargs.pop('environment')
        super().__init__(**kwargs)
        channels = self.environment.account.channels.all()
        self.fields['channels'].queryset = channels
        if self.instance:
            self.fields['channels'].initial = (k.replace(self.CHANNEL_PREFIX, '') for k in self.instance.channel_data)
        self.channel_forms = {
            channel : get_contact_form(channel)(
                prefix='%s%d' % (self.CHANNEL_PREFIX, channel.pk),
                data=kwargs.get('data'),
                files=kwargs.get('files'),
                initial=self.instance.channel_data.get('%s%d' % (self.CHANNEL_PREFIX, channel.pk), {})
                    if self.instance else {}
            )
            for channel in channels
        }

    def is_valid(self):
        if is_valid := super().is_valid():
            for channel in self.cleaned_data['channels']:
                is_valid = is_valid and self.channel_forms[channel].is_valid()
        return is_valid
           
    def save(self, commit=True):
        contact = super().save(commit=False)
        contact.environment = self.environment
        for channel in self.cleaned_data['channels']:
            form = self.channel_forms[channel]
            contact.channel_data[form.prefix] = form.cleaned_data

        if commit:
            contact.save()
        return contact

    class Meta:
        model = Contact
        fields = ('name', 'key', 'index1', 'index2', 'index3', 'index4', 'index5', 'index6')