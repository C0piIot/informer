from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.sites.models import Site

class Account(models.Model):
    name = models.CharField(_('name'), max_length=50)
    site = models.OneToOneField(Site, verbose_name=_('site'), on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(**kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')
