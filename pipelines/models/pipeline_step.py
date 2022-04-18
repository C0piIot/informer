from django.db import models
from django.utils.translation import gettext_lazy as _
from .pipeline import Pipeline

class PipelineStep(models.Model):
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
	
	class Meta:
		verbose_name = _('pipeline step')
		verbose_name_plural = _('pipeline steps')
		ordering = ('pipeline', 'order')