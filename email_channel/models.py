from django.db import models
from django.utils.translation import gettext_lazy as _
from configuration.models import Channel

class EmailChannel(Channel):
	host = models.CharField(_('host'), max_length=100)
	port = models.PositiveSmallIntegerField(_('port'))
	username = models.CharField(_('username'), max_length=150)
	password = models.CharField(_('password'), max_length=150)

	class Meta:
		verbose_name = _('email channel')
		verbose_name_plural = _('email channels')
		app_label = 'configuration'

class EmailTemplate(models.Model):
	subject = models.CharField(_('subject'), max_length=200)
	html_body = models.TextField(_('html body'))
	text_body = models.TextField(_('text_body'))

	class Meta:
		verbose_name = _('email template')
		verbose_name_plural = _('email templates')
