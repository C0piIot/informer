from django.db import models
from django.utils.translation import gettext_lazy as _
from .pipeline_step import PipelineStep

class Group(PipelineStep):
    TYPE = PipelineStep.GROUP
    window = models.DurationField(_('time window'))
    key = models.CharField(_('grouping key'), max_length=150)

    def __str__(self):
        return "Group by %s" % self.key