from django.db import models
from uuid import uuid4 
from django.utils.translation import gettext_lazy as _
from .pipeline import Pipeline

class PipelineRun(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid4, editable=False)
    account = models.ForeignKey('configuration.Account', on_delete=models.CASCADE, verbose_name=_('account'), editable=False)
    environment = models.ForeignKey('configuration.Environment', on_delete=models.CASCADE, verbose_name=_('environment'), editable=False)
    start = models.DateTimeField(_('start'), auto_now_add=True)
    trigger = models.CharField(_('trigger'), max_length=200, editable=False)
    pipeline = models.ForeignKey(Pipeline, on_delete=models.PROTECT, verbose_name=_('pipeline'), editable=False)
    contact_key = models.CharField(_('contact key'), max_length=100, editable=False)
    event_payload = models.JSONField(_('event payload'), default=dict, editable=False)
    pipeline_data = models.JSONField(_('pipeline data'), default=dict)


    class Meta:
        verbose_name = _('pipeline run')
        verbose_name_plural = _('pipeline runs')


    def __str__(self):
        return self.name


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
    def save_model(cls, environment, contact):
        contact.environment = environment
        contact.save()

    @classmethod
    def delete_model(cls, environment, key):
        pass