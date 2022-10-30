from django import forms
from django.utils.translation import gettext_lazy as _

class EmailContactForm(forms.Form):
    email = forms.EmailField(label=_('Email'), help_text=_('Flow steps using the channel email will deliver emails to this address'))