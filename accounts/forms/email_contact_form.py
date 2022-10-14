from django import forms
from django.utils.translation import gettext_lazy as _

class EmailContactForm(forms.Form):
    email = forms.EmailField(label=_('email'))