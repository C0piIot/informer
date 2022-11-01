from django.db import models
from uuid import uuid4 
from django.utils.translation import gettext_lazy as _
from .flow import Flow
from .flow_log import FlowLog
from django.utils.module_loading import import_string
from django.conf import settings
from django.urls import reverse
from django.contrib.sites.models import Site
import logging

logger = logging.getLogger()

class FlowRun(models.Model):
    _contact = None

    id = models.UUIDField(_('id'), primary_key=True, default=uuid4, editable=False)
    site = models.ForeignKey(Site, verbose_name=_('site'), on_delete=models.CASCADE, related_name='+', editable=False)
    environment = models.ForeignKey('accounts.Environment', on_delete=models.CASCADE, verbose_name=_('environment'),related_name='+', editable=False)
    start = models.DateTimeField(_('start'), auto_now_add=True)
    flow_revision = models.ForeignKey(Flow, on_delete=models.PROTECT, verbose_name=_('flow'), editable=False)
    flow_id = models.UUIDField(_('id'), editable=False)
    contact_key = models.CharField(_('contact key'), max_length=100)
    event_payload = models.JSONField(_('event payload'), default=dict, blank=True)
    flow_data = models.JSONField(_('flow data'), default=dict)
    group_key = models.CharField(_('group_key'), max_length=200, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.account = self.environment.account
        self.flow_id = self.flow_revision.id
        if not self.group_key:
            self.group_key = self.id.hex
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('flows:run', kwargs={ 'environment': self.environment.slug, 'id': self.flow_id, 'flow_run_id': self.id })

    class Meta:
        verbose_name = _('flow run')
        verbose_name_plural = _('flow runs')
        ordering = ('-start',)
        constraints = [models.UniqueConstraint(fields=('contact_key', 'flow_revision','group_key'), name='unique group')]

    def __str__(self):
        return _("Flow run %s") % self.id


    def log(self, level, message, context={}):
        logger.log(getattr(logging, level), message)
        import_string(settings.FLOW_LOG_STORAGE).save_flow_log(FlowLog(
            environment=self.environment,
            flow_run_id=self.id,
            level=level,
            message=message,
            context=context
        ))

    def get_logs(self):
        return import_string(settings.FLOW_LOG_STORAGE).get_flow_logs(self.account, self.pk)


    def contact(self):
        if self._contact is None:
            self._contact = import_string(settings.CONTACT_STORAGE).get_contact(self.environment, self.contact_key)
        return self._contact

    @classmethod
    def get_flow_runs(cls, environment, flow, start_key=None, amount=50, **filters):
        queryset = cls.objects.filter(environment=environment, flow_id=flow.id)
        if start_key is not None:
            queryset = queryset.filter(key__gt=start_key)
        return queryset[:amount]
        
    @classmethod
    def get_flow_run(cls, environment, id):
        return cls.objects.get(environment=environment, id=id)

    @classmethod
    def save_flow_run(cls, environment, model):
        model.environment = environment
        model.save()

    @classmethod
    def delete_flow_run(cls, environment, key):
        cls.objects.filter(environment=environment, key=key).delete()


    @classmethod
    def get_flow_group(cls, flow_run, group_key):
        try:
            return cls.objects.get(group_key=group_key, contact_key=flow_run.contact_key, flow_revision=flow_run.flow_revision)
        except FlowRun.DoesNotExist:
            flow_run.group_key = group_key
            return flow_run


    @classmethod
    def unset_group(cls, flow_run, group_key):
        flow_run.group_key = None
        

    def schedule_wake_up(self, flow_step, time_delta):
        import_string(settings.FLOW_EXECUTOR).schedule_wake_up(self, flow_step, time_delta)
