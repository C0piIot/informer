from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import time, date, datetime, timedelta


from .flow_step import FlowStep


class DoNotDisturb(FlowStep):

    class Meta:
        verbose_name = _("do not disturb")
        verbose_name_plural = _("do not disturb")
    ICON = "🤫"
    start = models.TimeField(_("start"))
    end = models.TimeField(_("end"))

    def step_run(self, flow_run):
        now = timezone.now()
        start = timezone.make_aware(datetime.combine(date.today(), self.start), is_dst=False)
        end = timezone.make_aware(datetime.combine(date.today(), self.end), is_dst=False)
        if end < start:
            end += timedelta(days=1)

        if start < now < end:
            flow_run.schedule_wake_up(self, end - now)
        else:
            self.run_next(flow_run)

    def step_wake_up(self, flow_run):
        self.run_next(flow_run)

    def clean(self):
        if self.start == self.end:
            raise ValidationError("Start and end times can't be the same")

    def __str__(self):
        return f"{super().__str__()} {self.start}-{self.end}"
