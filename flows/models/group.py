from django.db import models
from django.utils.translation import gettext_lazy as _
from .flow_step import FlowStep
from django.utils.module_loading import import_string
from django.conf import settings

class Group(FlowStep):
    icon = '⏬'
    DATA_KEY = 'GROUP_%s'
    window = models.DurationField(_('time window'))
    key = models.SlugField(_('grouping key'), max_length=150)

    def __str__(self):
        return "%s by %s ⏲️ %s" % (super().__str__(), self.key, self.window)

    def step_run(self, flow_run):
        key = self.DATA_KEY % self.key
        flow_group = import_string(settings.FLOW_RUN_STORAGE).get_flow_group(flow_run, self.key)
        
        if not key in flow_group.flow_data:
            flow_group.flow_data[key] = [flow_run.flow_data.copy()]
        else:
            flow_group.flow_data[key].append(flow_run.flow_data)

        if flow_run == flow_group:
            flow_run.schedule_wake_up(self, self.window)
        else:
            import_string(settings.FLOW_RUN_STORAGE).save_flow_run(flow_group.environment, flow_group)

    def step_wake_up(self, flow_run):
        import_string(settings.FLOW_RUN_STORAGE).unset_group(flow_run, self.key)
        self.run_next(flow_run)

    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groupings')