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
	)

	pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.CASCADE,
        verbose_name=_('pipeline'),
        related_name='steps'
    )
	order = models.PositiveSmallIntegerField(_('order'))
	type = models.CharField(_('type'), choices=TYPE_CHOICES, max_length=50)

	def __str__(self):
		return getattr(self, self.type).__str__()

	def save(self, *args, **kwargs):
		if self.TYPE:
			self.type = self.TYPE

		# We need to ensure we're calling save() from the child class
		if not hasattr(self, 'pipelinestep_ptr_id'):
			return getattr(self, self.type).save(*args, **kwargs)

		self.id = None
		self.pk = None
		self._state.adding = True
		super().save(*args, **kwargs)

	
	class Meta:
		verbose_name = _('pipeline step')
		verbose_name_plural = _('pipeline steps')
		ordering = ('pipeline', 'order')