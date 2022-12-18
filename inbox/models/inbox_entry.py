from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site
from contacts.models import RelatedContactModel
from uuid import uuid4

class InboxEntry(RelatedContactModel):
    key = models.UUIDField(_('key'), default=uuid4, primary_key=True, editable=False)
    date = models.DateTimeField(_('date'), auto_now_add=True)
    title = models.CharField(_('title'), max_length=100)
    message = models.TextField(_('message'))
    url = models.URLField(_('url'), blank=True, default='')
    image = models.URLField(_('image'), blank=True, default='')
    read = models.DateTimeField(_('read'), blank=True, null=True)
    entry_data = models.JSONField(_('entry data'), default=dict, help_text=_('Additional data for custom implementations'), blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('inbox entry')
        verbose_name_plural = _('inbox entries')
        indexes = (
            models.Index(fields=('site', 'environment', 'contact_key', '-date')),
        )
        ordering = ('-date',)