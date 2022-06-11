from django.db import models
from django.utils.translation import gettext_lazy as _
from .send_channel import SendChannel
from .pipeline_step import PipelineStep
from django.template import Template, Context



class Email(SendChannel):
    email_channel = models.ForeignKey('configuration.EmailChannel', on_delete=models.CASCADE, verbose_name=_('email channel'))
    subject = models.CharField(_('subject'), max_length=200)
    html_body = models.TextField(_('html body message'))
    text_body = models.TextField(_('plain text message'), help_text=_("Text used on clients that don't support html emails"))
    autogenerate_text = models.BooleanField(_('autogenerate text'), default=True, help_text="Generate text automatically from html template")
    from_email = models.EmailField(_('from email'), max_length=200, blank=True, help_text=_("From address for this step. Overrides channel's default from address"))

    def __str__(self):
        return "✉️ Email %s" % self.subject


    def run(self, pipeline_run):
        contact = pipeline_run.get_contact()
        key = str(self.email_channel.pk)

        if key in contact.channel_data:
            subject = Template(self.subject)
            text_body = Template(self.text_body)
            html_body = Template(self.html_body)

            html_context = Context(pipeline_run.event_payload)
            html_context.update({
                'contact': contact,
            })
            text_context = Context(pipeline_run.event_payload, autoescape=False)
            text_context.update({
                'contact': contact,
            })
            
            self.email_channel.send_mail(
                subject.render(text_context),
                text_body.render(text_context),
                html_body.render(html_context),
                self.from_email or self.email_channel.from_email,
                contact.channel_data[key]['email']
            )

    class Meta:
        verbose_name = _('email template')
        verbose_name_plural = _('email templates')