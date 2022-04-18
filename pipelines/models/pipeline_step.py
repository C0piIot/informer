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


	def save(self, *args, **kwargs):
		print(self.__class__ == PipelineStep)hay q arreglar esto
		if self.TYPE:
			self.type = self.TYPE
		self.id = None
		self.pk = None
		self._state.adding = True
		super().save(**kwargs)

	
	class Meta:
		verbose_name = _('pipeline step')
		verbose_name_plural = _('pipeline steps')
		ordering = ('pipeline', 'order')