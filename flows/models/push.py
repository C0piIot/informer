from django.db import models
from django.template import Context, Template
from django.utils.translation import gettext_lazy as _

from accounts.models import PushChannel

from .flow_log import FlowLog
from .flow_step import FlowStep


class Push(FlowStep):

    class Meta:
        verbose_name = _("send push")
        verbose_name_plural = _("push sending")
    ICON = "🔔"
    title = models.CharField(_("title"), max_length=200)
    body = models.TextField(_("body"))
    url = models.CharField(_("url"), max_length=500)

    def step_run(self, flow_run):
        if not (push_channel := PushChannel.objects.get(site=self.site)):
            flow_run.log(FlowLog.WARNING, "%s not sent: channel not configured")
            return self.run_next()

        if not push_channel.enabled:
            flow_run.log(FlowLog.WARNING, "%s not sent: channel disabled")
            return self.run_next()

        if not (
            channel_data := flow_run.contact.get_channel_data(
                push_channel.content_type.model
            )
        ):
            flow_run.log(
                FlowLog.INFO, "%s not sent: user doesn't have push channel data" % self
            )
            return self.run_next()

        title = Template(self.title)
        body = Template(self.body)
        url = Template(self.url)

        text_context = Context(flow_run.event_payload, autoescape=False)
        text_context.update(
            {
                "contact": flow_run.contact,
            }
        )

        response = push_channel.send_push(
            title.render(text_context),
            body.render(text_context),
            url.render(text_context),
            channel_data["fcm_tokens"],
        )
        flow_run.log(
            FlowLog.INFO,
            f'{self} successful sent to {sum(response.values())} of {len(response)} fcm tokens'
        )

        self.run_next(flow_run)

    def __str__(self):
        return '%s "%s"' % (super().__str__(), self.title)
