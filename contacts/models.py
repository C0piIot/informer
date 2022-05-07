from django.db import models
from django.utils.translation import gettext_lazy as _
from .contact_storage import ContactStorage

class Contact(models.Model):
    id = models.CharField(_('id'), max_length=100, primary_key=True)
    name = models.CharField(_('name'), max_length=150)

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