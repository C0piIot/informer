from django.db import models
from django.utils.translation import gettext_lazy as _
from .send_channel import SendChannel
from .pipeline_step import PipelineStep
from django.template import Template, Context
from .pipeline_log import PipelineLog

class Push(SendChannel):
    push_channel = models.ForeignKey('configuration.PushChannel', on_delete=models.CASCADE, verbose_name=_('push channel'))
    title = models.CharField(_('title'), max_length=200)
    body = models.TextField(_('body'))
    url = models.URLField(_('url'))
    
    def __str__(self):
        return "🔔 Push %s" % self.title


    def step_run(self, pipeline_run):
        contact = pipeline_run.contact()
        key = str(self.push_channel.pk)

        if key in contact.channel_data:
            title = Template(self.title)
            body = Template(self.body)
            url = Template(self.url)

            text_context = Context(pipeline_run.event_payload, autoescape=False)
            text_context.update({
                'contact': contact,
            })

            response = self.push_channel.send_push(
                title.render(text_context),
                body.render(text_context),
                url.render(text_context),
                contact.channel_data[key]['fcm_tokens']
            )
            pipeline_run.log(PipelineLog.INFO, "%s successful sent to %d of %d fcm tokens" % (self, sum(response.values()), len(response)))
        else:
            pipeline_run.log(PipelineLog.INFO, "%s not sent: user doesn't have channel data" % self)
            
        self.run_next(pipeline_run)

    class Meta:
        verbose_name = _('push template')
        verbose_name_plural = _('push templates')