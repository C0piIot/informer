from django.db import models
from django.utils.translation import gettext_lazy as _
from .pipeline_step import PipelineStep

class Delay(PipelineStep):
    time = models.DurationField(_('time'))

    def step_run(self, pipeline_run):
        pipeline_run.schedule_wake_up(self, self.time)


    def step_wake_up(self, pipeline_run):
        print("HOLA")

    def __str__(self):
        return "⏲️ Delay %s" % self.time
