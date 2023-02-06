from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.utils.translation import gettext_lazy as _

class LoginForm(AuthenticationForm):
	username = forms.EmailField(label=_("Email"))
