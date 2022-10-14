from django.db import models
from django.utils.translation import gettext_lazy as _
from .send_channel import SendChannel
from .flow_step import FlowStep
from django.template import Template, Context
from .flow_log import FlowLog

class Push(SendChannel):
    push_channel = models.ForeignKey('accounts.PushChannel', on_delete=models.CASCADE, verbose_name=_('push channel'))
    title = models.CharField(_('title'), max_length=200)
    body = models.TextField(_('body'))
    url = models.URLField(_('url'))
    
    def __str__(self):
        return "🔔 Push %s" % self.title


    def step_run(self, flow_run):
        contact = flow_run.contact()
        key = str(self.push_channel.pk)

        if key in contact.channel_data:
            title = Template(self.title)
            body = Template(self.body)
            url = Template(self.url)

            text_context = Context(flow_run.event_payload, autoescape=False)
            text_context.update({
                'contact': contact,
            })

            response = self.push_channel.send_push(
                title.render(text_context),
                body.render(text_context),
                url.render(text_context),
                contact.channel_data[key]['fcm_tokens']
            )
            flow_run.log(FlowLog.INFO, "%s successful sent to %d of %d fcm tokens" % (self, sum(response.values()), len(response)))
        else:
            flow_run.log(FlowLog.INFO, "%s not sent: user doesn't have channel data" % self)
            
        self.run_next(flow_run)

    class Meta:
        verbose_name = _('push template')
        verbose_name_plural = _('push templates')