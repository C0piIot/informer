from django.db import models
from django.utils.translation import gettext_lazy as _
from .pipeline_step import PipelineStep

class Group(PipelineStep):
    window = models.DurationField(_('time window'))
    key = models.CharField(_('grouping key'), max_length=150)

    def __str__(self):
        return "⏬ Group by %s" % self.key

    def step_run(self, pipeline_run):
        pipeline_run.schedule_wake_up(self, self.time)

    def step_wake_up(self, pipeline_run):
        self.run_next(pipeline_run)
