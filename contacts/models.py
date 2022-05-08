from django.db import models
from django.utils.translation import gettext_lazy as _
from .contact_storage import ContactStorage

class Contact(models.Model):
    id = models.CharField(_('id'), max_length=100, primary_key=True)
    index1 = models.CharField(_('index 1'), max_length=100, db_index=True)
    index2 = models.CharField(_('index 2'), max_length=100, db_index=True)
    index3 = models.CharField(_('index 3'), max_length=100, db_index=True)
    index4 = models.CharField(_('index 4'), max_length=100, db_index=True)
    index5 = models.CharField(_('index 5'), max_length=100, db_index=True)
    contact_data = models.JSONField(_('contact data'), default=dict)
    channel_data = models.JSONField(_('channel data'), default=dict)


    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')

    @classmethod
    def get_contacts(cls, start_key, amount=50, **filters):
        return cls.objects.filter(pk__gt=start_key)[:amount]
        
    @classmethod
    def get_contact(cls, key):
        pass

    @classmethod
    def save_contact(cls, contact):
        pass

    @classmethod
    def delete_contact(cls, key):
        pass