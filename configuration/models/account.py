from django.db import models
from django.utils.translation import gettext_lazy as _

class Account(models.Model):
    name = models.CharField(_('name'), max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')
