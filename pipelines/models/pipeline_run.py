from django.db import models
from uuid import uuid4 
from django.utils.translation import gettext_lazy as _
from .pipeline import Pipeline
from .pipeline_log import PipelineLog
from django.utils.module_loading import import_string
from django.conf import settings
import logging

logger = logging.getLogger()

class PipelineRun(models.Model):
    _contact = None

    id = models.UUIDField(_('id'), primary_key=True, default=uuid4, editable=False)
    account = models.ForeignKey('configuration.Account', on_delete=models.CASCADE, verbose_name=_('account'), editable=False)
    environment = models.ForeignKey('configuration.Environment', on_delete=models.CASCADE, verbose_name=_('environment'), editable=False)
    start = models.DateTimeField(_('start'), auto_now_add=True)
    pipeline_revision = models.ForeignKey(Pipeline, on_delete=models.PROTECT, verbose_name=_('pipeline'), editable=False)
    pipeline_id = models.UUIDField(_('id'), editable=False)
    contact_key = models.CharField(_('contact key'), max_length=100, editable=False)
    event_payload = models.JSONField(_('event payload'), default=dict, editable=False)
    pipeline_data = models.JSONField(_('pipeline data'), default=dict)
    group_key = models.CharField(_('group_key'), max_length=200, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.account = self.environment.account
        self.pipeline_id = self.pipeline_revision.id
        if not self.group_key:
            self.group_key = self.id.hex
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('pipeline run')
        verbose_name_plural = _('pipeline runs')
        ordering = ('-start',)
        constraints = [models.UniqueConstraint(fields=('contact_key', 'pipeline_revision','group_key'), name='unique group')]

    def __str__(self):
        return _("Pipeline run %s") % self.id


    def log(self, level, message, context={}):
        logger.log(getattr(logging, level), message)
        import_string(settings.PIPELINE_LOG_STORAGE).save_pipeline_log(PipelineLog(
            environment=self.environment,
            pipeline_run_id=self.id,
            level=level,
            message=message,
            context=context
        ))

    def get_logs(self):
        return import_string(settings.PIPELINE_LOG_STORAGE).get_pipeline_logs(self.account, self.pk)


    def contact(self):
        if self._contact is None:
            self._contact = import_string(settings.CONTACT_STORAGE).get_contact(self.environment, self.contact_key)
        return self._contact

    @classmethod
    def get_pipeline_runs(cls, environment, pipeline, start_key=None, amount=50, **filters):
        queryset = cls.objects.filter(environment=environment, pipeline_id=pipeline.id)
        if start_key is not None:
            queryset = queryset.filter(key__gt=start_key)
        return queryset[:amount]
        
    @classmethod
    def get_pipeline_run(cls, environment, id):
        return cls.objects.get(environment=environment, id=id)

    @classmethod
    def save_pipeline_run(cls, environment, model):
        model.environment = environment
        model.save()

    @classmethod
    def delete_pipeline_run(cls, environment, key):
        cls.objects.filter(environment=environment, key=key).delete()


    @classmethod
    def get_pipeline_group(cls, pipeline_run, group_key):
        try:
            return cls.objects.get(group_key=group_key, contact_key=self.contact_key, pipeline_revision=pipeline_revision)
        except PipelineRun.DoesNotExist:
            pipeline_run.group_key = group_key
            pipeline_run.save()
            return pipeline_run


    @classmethod
    def unset_group(cls, pipeline_run, group_key):
        pipeline_run.group_key = None
        pipeline_run.save()




    def schedule_wake_up(self, pipeline_step, time_delta):
        import_string(settings.PIPELINE_EXECUTOR).schedule_wake_up(self, pipeline_step, time_delta)


    @classmethod
    def dispatch_event(cls, environment, contact, event, event_payload={}):
        for pipeline in Pipeline.objects.filter(environments=environment, trigger=event, enabled=True):
            pipeline_run = cls(
                pipeline_revision=pipeline,
                contact_key=contact.key,
                event_payload=event_payload,
            )
            pipeline_run.contact = contact
            import_string(settings.PIPELINE_RUN_STORAGE).save_pipeline_run(environment, pipeline_run)
            import_string(settings.PIPELINE_EXECUTOR).run(pipeline_run)
