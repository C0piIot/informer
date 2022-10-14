from django.db import models
from django.utils.translation import gettext_lazy as _
from .flow_step import FlowStep
from django.template import Template, Context
from .flow_log import FlowLog
from accounts.models import PushChannel

class Push(FlowStep):
    title = models.CharField(_('title'), max_length=200)
    body = models.TextField(_('body'))
    url = models.URLField(_('url'))
    testing_context = models.JSONField(_('testing context'), default=dict)
    
    def __str__(self):
        return "🔔 Push %s" % self.title


    def step_run(self, flow_run):
        contact = flow_run.contact()
        push_channel = PushChannel.objects.get(account=self.account)
        key = str(push_channel.pk)

        if key in contact.channel_data:
            title = Template(self.title)
            body = Template(self.body)
            url = Template(self.url)

            text_context = Context(flow_run.event_payload, autoescape=False)
            text_context.update({
                'contact': contact,
            })

            response = push_channel.send_push(
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
        verbose_name = _('send push')
        verbose_name_plural = _('push sending')