from django.db import models
from django.utils.translation import gettext_lazy as _
from .flow_step import FlowStep
from urllib.parse import urlparse
from django.template import Template, Context
from urllib import request


class Webhook(FlowStep):
    ICON = '🌐'
    CONTENT_TYPES = ('application/x-www-form-urlencoded', 'application/json', 'application/xml', 'text/plain', 'text/html')
    METHODS = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE',)
    url = models.URLField(_('url'))
    method = models.CharField(_('method'), max_length=6, choices=((m, m) for m in METHODS))
    contenttype = models.CharField(_('Content type'), max_length=50, choices=((e, e) for e in CONTENT_TYPES))
    body = models.TextField(_('body'), blank=True)
    preview_context = models.JSONField(_('preview context'), blank=True, default=dict)

    def __str__(self):
        return "%s %s %s" % (super().__str__(), self.method, urlparse(self.url).netloc)

    def step_run(self, flow_run):

        contact = flow_run.contact()
        context = Context(flow_run.event_payload, autoescape=False)
        context.update({
            'contact': contact,
        })

        body = Template(self.body).render(context)
        url = Template(self.url).render(context)

        req = request.Request(url.render(context), 
            headers={'Content-Type': self.contenttype },
            method=self.method,
            data=body.render(context))

        response = request.urlopen(req)

        low_run.log(FlowLog.INFO, "Webhook %s response: %s" % (r, response.getcode()))
        
        self.run_next(flow_run)


    class Meta:
        verbose_name = _('webook')
        verbose_name_plural = _('webhooks')

