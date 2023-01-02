from django.db import models
from flows.models import FlowLog
from django.utils.translation import gettext_lazy as _
from flows.models import FlowStep
from .inbox_entry import InboxEntry
from django.utils.module_loading import import_string

class Inbox(FlowStep):
    ICON = '📥'
    title = models.CharField(_('title'), max_length=100)
    message = models.TextField(_('message'))
    url = models.URLField(_('url'), blank=True, default='')
    image = models.URLField(_('image'), blank=True, default='')
    entry_data = models.JSONField(_('entry data'), default=dict, help_text=_('Additional data for custom implementations'), blank=True)
    preview_context = models.JSONField(_('preview context'), blank=True, default=dict)

    def __str__(self):
        return "%s \"%s\"" % (super().__str__(), self.title)

    def step_run(self, flow_run):
        text_context = Context(flow_run.event_payload, autoescape=False)
        title = Template(self.title)
        message = Template(self.message)
        url = Template(self.url)
        image = Template(self.image)
        entry_data = Template(self.entry_data)

        inbox_entry = InboxEntry(
            site=flow_run.site,
            environment=flow_run.environment,
            contact_key=flow_run.contact.key,
            title=title.render(text_context),
            message=message.render(text_context),
            url=url.render(text_context),
            image=image.render(text_context),
            entry_data=entry_data.render(text_context)
        )
        import_string(settings.FLOW_LOG_STORAGE).save_entry(flow_run.environment, inbox_entry)
        flow_run.log(FlowLog.INFO, "Inbox entry %s created" % str(inbox_entry.key))
        self.run_next(flow_run)

    class Meta:
        verbose_name = _('send to inbox')
        verbose_name_plural = _('sending to inbox')