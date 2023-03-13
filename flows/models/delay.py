from django.db import models
from django.utils.translation import gettext_lazy as _

from .flow_step import FlowStep


class Delay(FlowStep):
    class Meta:
        verbose_name = _("delay")
        verbose_name_plural = _("delays")

    ICON = "⏲️"
    time = models.DurationField(_("time"))

    def step_run(self, flow_run):
        flow_run.schedule_wake_up(self, self.time)

    def step_wake_up(self, flow_run):
        self.run_next(flow_run)

    def __str__(self):
        return f"{super().__str__()} {self.time}"
