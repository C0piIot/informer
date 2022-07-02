from django.db import models
from django.utils.translation import gettext_lazy as _
from .pipeline_step import PipelineStep
from django.utils.module_loading import import_string
from django.conf import settings

class Group(PipelineStep):
    DATA_KEY = 'GROUP-%s'
    window = models.DurationField(_('time window'))
    key = models.SlugField(_('grouping key'), max_length=150)

    def __str__(self):
        return "⏬ Group by %s" % self.key

    def step_run(self, pipeline_run):
        key = self.DATA_KEY % self.key
        pipeline_group = import_string(settings.PIPELINE_RUN_STORAGE).get_pipeline_group(cls, pipeline_run, self.key)
        
        if not key in pipeline_group.pipeline_data:
            pipeline_group.pipeline_data[key] = list(pipeline_group.pipeline_data)
        else:
            pipeline_group.pipeline_data[key].append(pipeline_group.pipeline_data)

        if pipeline_run == pipeline_group:
            pipeline_run.schedule_wake_up(self, self.time)

    def step_wake_up(self, pipeline_run):
        import_string(settings.PIPELINE_RUN_STORAGE).unset_group(cls, pipeline_run, self.key)
        self.run_next(pipeline_run)
