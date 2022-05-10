from django.db import models
from django.utils.translation import gettext_lazy as _
from .contact_storage import ContactStorage
from uuid import uuid4 

class Contact(models.Model):
    id = models.CharField(_('id'), max_length=100)
    name = models.CharField(_('name'), max_length=200)
    revision = models.UUIDField(_('revision'), primary_key=True, default=uuid4, editable=False)
    environments = models.ManyToManyField('configuration.Environment', related_name='contacts',)
    index1 = models.CharField(_('index 1'), max_length=100,)
    index2 = models.CharField(_('index 2'), max_length=100,)
    index3 = models.CharField(_('index 3'), max_length=100,)
    index4 = models.CharField(_('index 4'), max_length=100,)
    index5 = models.CharField(_('index 5'), max_length=100,)
    contact_data = models.JSONField(_('contact data'), default=dict)
    channel_data = models.JSONField(_('channel data'), default=dict)

    def save(self, *args, **kwargs):
        self.pk = uuid4()
        self._state.adding = True
        super().save(**kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')
        unique_together = (
            ('environment', 'id'),
            ('environment', 'index1'),
            ('environment', 'index2'),
            ('environment', 'index3'),
            ('environment', 'index4'),
            ('environment', 'index5'),
        )


    @classmethod
    def get_contacts(cls, environment, start_key, amount=50, **filters):
        return cls.objects.filter(pk__gt=start_key)[:amount]
        
    @classmethod
    def get_contact(cls, environment, id):
        pass

    @classmethod
    def save_contact(cls, environment, contact):
        pass

    @classmethod
    def delete_contact(cls, environment, id):
        pass