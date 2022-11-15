from django import forms
from django.utils.translation import gettext_lazy as _

class ContactSearchForm(forms.Form):
	filter_key = forms.CharField(label=_('Key'), required=False)
	filter_name = forms.CharField(label=_('Name'), required=False)
