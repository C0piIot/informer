from django.db import models
from django.utils.translation import gettext_lazy as _
from .pipeline_step import PipelineStep

class Group(PipelineStep):
	window = models.DurationField(_('time window'))
	key = models.CharField(_('grouping key'), max_length=150)