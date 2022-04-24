from django.db import models
from django.utils.translation import gettext_lazy as _
from .send_channel import SendChannel

class SendEmail(SendChannel):
	email_channel = models.ForeignKey('configuration.EmailChannel', on_delete=models.CASCADE)
	subject = models.CharField(_('subject'), max_length=200)
	html_body = models.TextField(_('html body'))
	text_body = models.TextField(_('text_body'))

	class Meta:
		verbose_name = _('email template')
		verbose_name_plural = _('email templates')