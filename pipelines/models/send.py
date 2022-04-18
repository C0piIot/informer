from django.db import models
from django.utils.translation import gettext_lazy as _
from .pipeline_step import PipelineStep

class Send(PipelineStep):
	channel = models.ForeignKey('configuration.Channel', on_delete=models.PROTECT)
	only_unread = models.BooleanField(_('unread only'), default=True)