from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4 

class Contact(models.Model):
    key = models.CharField(_('key'), max_length=100, help_text=_('Key must be unique to all your contacts'))
    name = models.CharField(_('name'), max_length=200, help_text=_('This name will be used across informer app'))
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, verbose_name=_('account'), editable=False)
    environment = models.ForeignKey('accounts.Environment', on_delete=models.CASCADE, verbose_name=_('environment'), editable=False)
    index1 = models.CharField(_('index 1'), max_length=100, blank=True)
    index2 = models.CharField(_('index 2'), max_length=100, blank=True)
    index3 = models.CharField(_('index 3'), max_length=100, blank=True)
    index4 = models.CharField(_('index 4'), max_length=100, blank=True)
    index5 = models.CharField(_('index 5'), max_length=100, blank=True)
    index6 = models.CharField(_('index 6'), max_length=100, blank=True)
    contact_data = models.JSONField(_('contact data'), default=dict, help_text=_('Contact data will be available for use in flow templates'))
    channel_data = models.JSONField(_('channel data'), default=dict)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.account = self.environment.account
        super().save(*args, **kwargs)

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

    @classmethod
    def get_contacts(cls, environment, start_key=None, amount=50, **filters):
        queryset = cls.objects.filter(environment=environment)
        if start_key is not None:
            queryset = queryset.filter(key__gt=start_key)
        return queryset[:amount]
        
    @classmethod
    def get_contact(cls, environment, key):
        return cls.objects.filter(environment=environment, key=key).first()

    @classmethod
    def save_contact(cls, environment, contact):
        contact.environment = environment
        contact.save()

    @classmethod
    def delete_contact(cls, environment, key):
        cls.objects.filter(environment=environment, key=key).delete()