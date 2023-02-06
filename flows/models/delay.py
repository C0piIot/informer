from django.db import models
from django.utils.translation import gettext_lazy as _
from .flow_step import FlowStep

class Delay(FlowStep):

    ICON = '⏲️';
    time = models.DurationField(_('time'))

    def step_run(self, flow_run):
        flow_run.schedule_wake_up(self, self.time)


    def step_wake_up(self, flow_run):
        self.run_next(flow_run)

    class Meta:
        verbose_name = _('delay')
        verbose_name_plural = _('delays')

    def __str__(self):
        return "%s %s" % (super().__str__(), self.time)
