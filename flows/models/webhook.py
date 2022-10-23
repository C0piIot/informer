from django.db import models
from django.utils.translation import gettext_lazy as _
from .flow_step import FlowStep
from urllib.parse import urlparse

class Webhook(FlowStep):
    ICON = '🌐'
    CONTENT_TYPES = ('application/x-www-form-urlencoded', 'application/json', 'application/xml', 'text/plain', 'text/html')
    METHODS = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE',)
    url = models.URLField(_('url'))
    method = models.CharField(_('method'), max_length=6, choices=((m, m) for m in METHODS))
    content_type = models.CharField(_('Content type'), max_length=50, choices=((e, e) for e in ENCODINGS))
    body = models.CharField(_('body'), blank=True)

    def __str__(self):
        return "%s %s %s" % (super().__str__(), self.method, urlparse(self.url).netloc)

    def step_run(self, flow_run):
        flow_run.schedule_wake_up(self, self.time)

    class Meta:
        verbose_name = _('webook')
        verbose_name_plural = _('webhooks')

