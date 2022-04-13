from django.db import models
from django.utils.translation import gettext_lazy as _

class Pipeline(models.Model):
	date = models.DateTimeField(_('date'), auto_now_add=True)
	environments = models.ManyToManyField('configuration.Environment', related_name='pipelines')
	name = models.CharField(_('name'), max_length=150, unique=True)
	enabled = models.BooleanField(_('enabled'), default=True)
	trigger = models.CharField(_('trigger'), max_length=150, db_index=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _('pipeline')
		verbose_name_plural = _('pipelines')
		ordering = ('name',)