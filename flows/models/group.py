from django.conf import settings
from django.db import models
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from .flow_step import FlowStep


class Group(FlowStep):
    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groupings")

    ICON = "⏬"
    DATA_KEY = "GROUP_%s"
    window = models.DurationField(
        _("time window"),
        help_text=_(
            "All flows for the same user will be merged "
            "withint the time window started with the first one"
        ),
    )
    key = models.SlugField(
        _("grouping key"),
        max_length=150,
        help_text=_(
            "Context data from each flow will be available "
            "in an array with the name GROUP_{grouping key}"
        ),
    )

    def step_run(self, flow_run):
        key = self.DATA_KEY % self.key
        flow_group = import_string(settings.FLOW_RUN_STORAGE).get_flow_group(
            flow_run, self.key
        )

        if not key in flow_group.flow_data:
            flow_group.flow_data[key] = [flow_run.flow_data.copy()]
        else:
            flow_group.flow_data[key].append(flow_run.flow_data)

        if flow_run == flow_group:
            flow_run.schedule_wake_up(self, self.window)
        else:
            import_string(settings.FLOW_RUN_STORAGE).save_flow_run(
                flow_group.environment, flow_group
            )

    def step_wake_up(self, flow_run):
        import_string(settings.FLOW_RUN_STORAGE).unset_group(
            flow_run, self.key)
        self.run_next(flow_run)

    def __str__(self):
        return f"{super().__str__()} by {self.key} ⏲️ {self.window}"
