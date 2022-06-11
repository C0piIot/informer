from django import forms
from django.utils.translation import gettext_lazy as _
from contacts.models import Contact 
from configuration.models import Channel
from configuration.forms import get_contact_form
from django.utils.module_loading import import_string
from django.conf import settings

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
            self.fields['channels'].initial = self.instance.channel_data.keys()
        self.channel_forms = {
            channel : get_contact_form(channel)(
                prefix='%s%d' % (self.CHANNEL_PREFIX, channel.pk),
                data=kwargs.get('data'),
                files=kwargs.get('files'),
                initial=self.instance.channel_data.get(str(channel.pk), {})
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
        contact.channel_data = {}
        for channel in self.cleaned_data['channels']:
            form = self.channel_forms[channel]
            contact.channel_data[str(channel.pk)] = form.cleaned_data
        if commit:
            import_string(settings.CONTACT_STORAGE).save_model(self.environment, contact)
        return contact

    class Meta:
        model = Contact
        fields = ('name', 'key', 'index1', 'index2', 'index3', 'index4', 'index5', 'index6')