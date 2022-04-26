from django.db import models
from django.utils.translation import gettext_lazy as _
from .pipeline_step import PipelineStep

class SendChannel(PipelineStep):
	only_unread = models.BooleanField(_('unread only'), default=True)

	class Meta:
		abstract = True