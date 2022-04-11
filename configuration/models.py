from django.db import models
from django.utils.translation import gettext_lazy as _


class Environment(models.Model):
	name = models.CharField(_('name'), max_length=150, unique=True)


class Channel(models.Model):
	name = models.CharField(_('name'), max_length=100, unique=True)
	enabled = models.BooleanField(_('enabled'), default=True)

	class Meta:
		ordering = ('name',)
		verbose_name = _('channel')
		verbose_name_plural = _('channels')

