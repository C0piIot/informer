from django.db import models
from django.utils.translation import gettext_lazy as _
from .send_channel import SendChannel

class Email(SendChannel):
	email_channel = models.ForeignKey('configuration.EmailChannel', on_delete=models.CASCADE)
	subject = models.CharField(_('subject'), max_length=200)
	html_body = models.TextField(_('html body message'))
	text_body = models.TextField(_('plain text message'), help_text=_("Text used on clients that don't support html emails"))
	autogenerate_text = models.BooleanField(_('autogenerate text'), default=True, help_text="Generate text automatically from html template")

	class Meta:
		verbose_name = _('email template')
		verbose_name_plural = _('email templates')