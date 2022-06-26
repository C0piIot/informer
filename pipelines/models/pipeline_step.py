from django.db import models
from uuid import uuid4 
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from .pipeline import Pipeline
from .pipeline_log import PipelineLog

class PipelineStep(models.Model):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, verbose_name=_('pipeline'), related_name='steps', editable=False)
    account = models.ForeignKey('configuration.Account', on_delete=models.CASCADE, verbose_name=_('account'), editable=False)
    order = models.PositiveSmallIntegerField(_('order'), editable=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, editable=False)

    def get_typed_instance(self):
        return getattr(self, self.content_type.model)

    def __str__(self):
        return self.get_typed_instance().__str__()

    def save(self, *args, **kwargs):
        if not self.content_type_id:
            content_type = ContentType.objects.get_for_model(self, for_concrete_model=True)
            if content_type.model_class() != PipelineStep:
                self.content_type = content_type
        self.account = self.pipeline.account
        self.id = None
        self.pk = None
        self._state.adding = True
        super().save(*args, **kwargs)

    def run_next(self, pipeline_run):
        if next_step := PipelineStep.objects.filter(pipeline=self.pipeline, order__gt=self.order).first():
            next_step.run(pipeline_run)
        else:
            pipeline_run.log(PipelineLog.INFO, 'Last step reached')


    def run(self, pipeline_run):
        typed_instance = self.get_typed_instance()
        pipeline_run.log(PipelineLog.INFO, 'Running pipeline step %s' % typed_instance)
        return typed_instance.step_run(pipeline_run)

    def wake_up(self, pipeline_run):
        typed_instance = self.get_typed_instance()
        pipeline_run.log(PipelineLog.INFO, 'Waking up pipeline step %s' % typed_instance)
        return typed_instance.step_wake_up(pipeline_run)        


    class Meta:
        verbose_name = _('pipeline step')
        verbose_name_plural = _('pipeline steps')
        ordering = ('pipeline', 'order')
        unique_together = ('pipeline', 'order')