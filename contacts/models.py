from django.db import models
from django.utils.translation import gettext_lazy as _
from .contact_storage import ContactStorage
from uuid import uuid4 

class Contact(models.Model):
    key = models.CharField(_('key'), max_length=100)
    name = models.CharField(_('name'), max_length=200)
    environment = models.ForeignKey('configuration.Environment', on_delete=models.CASCADE, verbose_name=_('environment'), editable=False)
    index1 = models.CharField(_('index 1'), max_length=100,)
    index2 = models.CharField(_('index 2'), max_length=100,)
    index3 = models.CharField(_('index 3'), max_length=100,)
    index4 = models.CharField(_('index 4'), max_length=100,)
    index5 = models.CharField(_('index 5'), max_length=100,)
    contact_data = models.JSONField(_('contact data'), default=dict)
    channel_data = models.JSONField(_('channel data'), default=dict)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')
        unique_together = (
            ('environment', 'key'),
            ('environment', 'index1'),
            ('environment', 'index2'),
            ('environment', 'index3'),
            ('environment', 'index4'),
            ('environment', 'index5'),
        )


    @classmethod
    def get_contacts(cls, environment, start_key, amount=50, **filters):
        return cls.objects.filter(environment=environment, key__gt=start_key)[:amount]
        
    @classmethod
    def get_contact(cls, environment, key):
        pass

    @classmethod
    def save_contact(cls, environment, contact):
        pass

    @classmethod
    def delete_contact(cls, environment, key):
        pass