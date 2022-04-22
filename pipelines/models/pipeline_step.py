from django.db import models
from uuid import uuid4 
from django.utils.translation import gettext_lazy as _
from .pipeline import Pipeline

class PipelineStep(models.Model):
	TYPE = None

	DELAY = 'delay'
	GROUP = 'group'
	SEND = 'send'

	TYPE_CHOICES = (
		(DELAY, _('delay')),
		(GROUP, _('group')),
	)

	pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.CASCADE,
        verbose_name=_('pipeline'),
        related_name='steps'
    )
	order = models.PositiveSmallIntegerField(_('order'))
	type = models.CharField(_('type'), choices=TYPE_CHOICES, max_length=50)

	def get_typed_instance(self):
		return getattr(self, self.type)

	def __str__(self):
		return get_typed_instance().__str__()

	def save(self, *args, **kwargs):
		if self.TYPE:
			self.type = self.TYPE

		self.id = None
		self.pk = None
		self._state.adding = True
		super().save(*args, **kwargs)

	
	class Meta:
		verbose_name = _('pipeline step')
		verbose_name_plural = _('pipeline steps')
		ordering = ('pipeline', 'order')