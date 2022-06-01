from django.db import models
from uuid import uuid4 
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from .pipeline import Pipeline

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

    def run(self, pipeline_run):
        return self.get_typed_instance().run()


    class Meta:
        verbose_name = _('pipeline step')
        verbose_name_plural = _('pipeline steps')
        ordering = ('pipeline', 'order')
        unique_together = ('pipeline', 'order')