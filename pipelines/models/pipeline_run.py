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
    contact = None

    id = models.UUIDField(_('id'), primary_key=True, default=uuid4, editable=False)
    account = models.ForeignKey('configuration.Account', on_delete=models.CASCADE, verbose_name=_('account'), editable=False)
    environment = models.ForeignKey('configuration.Environment', on_delete=models.CASCADE, verbose_name=_('environment'), editable=False)
    start = models.DateTimeField(_('start'), auto_now_add=True)
    pipeline = models.ForeignKey(Pipeline, on_delete=models.PROTECT, verbose_name=_('pipeline'), editable=False)
    contact_key = models.CharField(_('contact key'), max_length=100, editable=False)
    event_payload = models.JSONField(_('event payload'), default=dict, editable=False)
    pipeline_data = models.JSONField(_('pipeline data'), default=dict)

    def save(self, *args, **kwargs):
        self.account = self.environment.account
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('pipeline run')
        verbose_name_plural = _('pipeline runs')

    def __str__(self):
        return self.name


    def log(self, level, message, context={}):
        logger.log(getattr(logging, level), message)
        import_string(settings.PIPELINE_LOG_STORAGE).save_model(PipelineLog(
            environment=self.environment,
            pipeline_run_id=self.id,
            level=level,
            message=message,
            context=context
        ))


    def get_contact(self):
        if self.contact is None:
            self.contact = import_string(settings.CONTACT_STORAGE).get_model(self.environment, self.contact_key)
        return self.contact

    @classmethod
    def get_models(cls, environment, start_key=None, amount=50, **filters):
        queryset = cls.objects.filter(environment=environment)
        if start_key is not None:
            queryset = queryset.filter(key__gt=start_key)
        return queryset[:amount]
        
    @classmethod
    def get_model(cls, environment, key):
        return cls.objects.get(environment=environment, key=key)

    @classmethod
    def save_model(cls, environment, model):
        model.environment = environment
        model.save()

    @classmethod
    def delete_model(cls, environment, key):
        cls.objects.filter(environment=environment, key=key).delete()


    @classmethod
    def dispatch_event(cls, environment, contact, event, event_payload={}):
        for pipeline in Pipeline.objects.filter(environments=environment, trigger=event, enabled=True):
            pipeline_run = cls(
                pipeline=pipeline,
                contact_key=contact.key,
                event_payload=event_payload,
            )
            pipeline_run.contact = contact
            import_string(settings.PIPELINE_STORAGE).save_model(environment, pipeline_run)

            if step := pipeline.steps.first():
                import_string(settings.PIPELINE_EXECUTOR).execute_step(step, pipeline_run)
            else:
                pipeline_run.log(PipelineLog.WARNING, 'No steps in current pipeline')
