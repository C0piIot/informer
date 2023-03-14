"""Inbox flow step for adding messages to a user inbox. Every inbox message is an InboxEntry."""
import json
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.template import Context, Template
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _

from contacts.models import RelatedContactModel
from flows.models import FlowLog, FlowStep


class InboxEntry(RelatedContactModel):
    """A message on a use inbox"""
    class Meta:
        verbose_name = _("inbox entry")
        verbose_name_plural = _("inbox entries")
        indexes = (
            models.Index(fields=("site", "environment",
                         "contact_key", "-date")),
        )
        ordering = ("-date",)

    key = models.UUIDField(_("key"), default=uuid4,
                           primary_key=True, editable=False)
    date = models.DateTimeField(_("date"), auto_now_add=True)
    title = models.CharField(_("title"), max_length=100)
    message = models.TextField(_("message"))
    url = models.URLField(_("url"), blank=True, default="")
    image = models.URLField(_("image"), blank=True, default="")
    read = models.DateTimeField(_("read"), blank=True, null=True)
    entry_data = models.JSONField(
        _("entry data"),
        default=dict,
        help_text=_("Additional data for custom implementations"),
        blank=True,
    )

    def __str__(self):
        return str(self.message)


class Inbox(FlowStep):
    """Flow step for creating inbox entries"""
    class Meta:
        verbose_name = _("send to inbox")
        verbose_name_plural = _("sending to inbox")

    ICON = "📥"
    title = models.CharField(_("title"), max_length=100)
    message = models.TextField(_("message"))
    url = models.URLField(_("url"), blank=True, default="")
    image = models.URLField(_("image"), blank=True, default="")
    entry_data = models.JSONField(
        _("entry data"),
        default=dict,
        help_text=_("Additional data for custom implementations"),
        blank=True,
    )

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
            entry_data=json.loads(entry_data.render(text_context)),
        )
        import_string(settings.INBOX_ENTRY_STORAGE).save_entry(inbox_entry)
        flow_run.log(FlowLog.INFO, "Inbox entry %s created" %
                     str(inbox_entry.key))
        self.run_next(flow_run)

    def __str__(self):
        return '%s "%s"' % (super().__str__(), self.title)
