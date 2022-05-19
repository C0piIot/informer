from django import forms
from django.utils.translation import gettext_lazy as _
from contacts.models import Contact 
from configuration.models import Channel
from configuration.forms import get_contact_form

class ContactForm(forms.ModelForm):

    environment = None
    channel_forms = None

    def __init__(self, **kwargs):
        self.environment = kwargs.pop('environment')
        super().__init__(**kwargs)
        self.channel_forms = {
            channel : get_contact_form(channel)()
            for channel in self.environment.account.channels.all()
        }
        
    def save(self, commit=True):
        contact = super().save(commit=False)
        contact.environment = self.environment
        if commit:
            contact.save()
        return contact


    class Meta:
        model = Contact
        fields = ('name', 'contact_data', 'index1', 'index2', 'index3', 'index4', 'index5', 'index6')
        widgets = { 'contact_data' : forms.HiddenInput }
