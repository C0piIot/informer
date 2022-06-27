from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4 

class PipelineLog(models.Model):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING ='WARNING'
    ERROR = 'ERROR'

    LEVEL_CHOICES = (
        (DEBUG, _('debug')),
        (INFO, _('info')),
        (WARNING, _('warning')),
        (ERROR, _('error')),
    )

    id = models.UUIDField(_('id'), default=uuid4, primary_key=True, editable=False)
    account = models.ForeignKey('configuration.Account', on_delete=models.CASCADE, verbose_name=_('account'), editable=False)
    environment = models.ForeignKey('configuration.Environment', on_delete=models.CASCADE, verbose_name=_('environment'), editable=False)
    pipeline_run_id = models.UUIDField(_('pipeline_run_id'))
    date = models.DateTimeField(_('date'), auto_now_add=True)
    level = models.CharField(_('level'), max_length=10, default=INFO, choices=LEVEL_CHOICES)
    message = models.CharField(_('message'), max_length=400)
    context = models.JSONField(_('context'), default=dict)


    def __str__(self):
        return "%s %s %s" % (self.date, self.level, self.message,)

    class Meta:
        verbose_name = _('pipeline log')
        verbose_name_plural = _('pipeline logs')
        ordering = ('date',)
        indexes = (
            models.Index(fields=('pipeline_run_id', '-date')),
           )


    @classmethod
    def save_pipeline_log(cls, log):
        log.account = log.environment.account
        log.save()


    @classmethod
    def get_pipeline_logs(cls, account, pipeline_run_id):
        return cls.objects.filter(account=account, pipeline_run_id=pipeline_run_id)

