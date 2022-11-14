from django.db import models
from django.utils.translation import gettext_lazy as _
from .flow_step import FlowStep
from django.template import Template, Context
from premailer import Premailer
from .flow_log import FlowLog
from accounts.models import EmailChannel
from django.contrib.sites.managers import CurrentSiteManager

class Email(FlowStep):
    objects = CurrentSiteManager

    ICON = "✉️"
    subject = models.CharField(_('subject'), max_length=200)
    html_body = models.TextField(_('html body message'))
    text_body = models.TextField(_('plain text message'), help_text=_("Text used on clients that don't support html emails"))
    autogenerate_text = models.BooleanField(_('autogenerate text'), default=True, help_text="Generate text automatically from html template")
    from_email = models.EmailField(_('from email'), max_length=200, blank=True, help_text=_("From address for this step. Overrides channel's default from address"))
    premailer = Premailer()
    preview_context = models.JSONField(_('preview context'), blank=True, default=dict)

    def __str__(self):
        return "%s %s" % (super().__str__(), self.subject)

    def step_run(self, flow_run):
        contact = flow_run.contact()
        email_channel = EmailChannel.objects.get(site=self.site)
        key = str(email_channel.pk)

        if key in contact.channel_data:
            subject = Template(self.subject)
            text_body = Template(self.text_body)
            html_body = Template(self.html_body)

            context = flow_run.event_payload.copy()
            context.update({ 'contact': contact })
            context.update(flow_run.flow_data)

            html_context = Context(context)
            text_context = Context(context, autoescape=False)
            
            email_channel.send_mail(
                subject.render(text_context),
                text_body.render(text_context),
                self.premailer.transform(html_body.render(html_context)),
                self.from_email or email_channel.from_email,
                contact.channel_data[key]['email']
            )
        else:
            flow_run.log(FlowLog.INFO, "%s not sent: user doesn't have channel data" % self)
            
        self.run_next(flow_run)

    class Meta:
        verbose_name = _('send email')
        verbose_name_plural = _('email sending')