from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4 
from django.contrib.sites.models import Site

class Contact(models.Model):

    key = models.CharField(_('key'), max_length=100, help_text=_('Key must be unique to all your contacts'))
    name = models.CharField(_('name'), max_length=200, help_text=_('This name will be used across informer app'))
    site = models.ForeignKey(Site, verbose_name=_('site'), on_delete=models.CASCADE, related_name='+', editable=False)
    environment = models.ForeignKey('accounts.Environment', on_delete=models.CASCADE, verbose_name=_('environment'), related_name='+', editable=False)
    index1 = models.CharField(_('index 1'), max_length=100, blank=True)
    index2 = models.CharField(_('index 2'), max_length=100, blank=True)
    index3 = models.CharField(_('index 3'), max_length=100, blank=True)
    index4 = models.CharField(_('index 4'), max_length=100, blank=True)
    index5 = models.CharField(_('index 5'), max_length=100, blank=True)
    index6 = models.CharField(_('index 6'), max_length=100, blank=True)
    contact_data = models.JSONField(_('contact data'), default=dict, help_text=_('Contact data will be available for use in flow templates'), blank=True)
    channel_data = models.JSONField(_('channel data'), default=dict)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.site = self.environment.site
        super().save(*args, **kwargs)

    def set_channel_data(self, channel_type, data):
        self.channel_data[channel_type] = data

    def get_channel_data(self, channel_type):
        return self.channel_data.get(channel_type, {})

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')
        constraints = (models.UniqueConstraint('environment', 'key', name="key_environment"),)
        indexes = (
            models.Index(fields=('environment', 'index1')),
            models.Index(fields=('environment', 'index2')),
            models.Index(fields=('environment', 'index3')),
            models.Index(fields=('environment', 'index4')),
            models.Index(fields=('environment', 'index5')),
            models.Index(fields=('environment', 'index6')),
        )
