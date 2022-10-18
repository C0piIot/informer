from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from rest_framework.authtoken.models import Token
from .account import Account


class Environment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_('account'), editable=False, related_name='environments')
    name = models.CharField(_('name'), max_length=50)
    slug = models.SlugField(_('slug'), editable=False)
    private_key = models.CharField(_('private key'), max_length=40, unique=True)
    public_key = models.CharField(_('public key'), max_length=40, unique=True)

    def get_absolute_url(self):
        return reverse('flows:list', kwargs={ 'environment': self.slug })

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.private_key:
            self.private_key = Token.generate_key()
        if not self.public_key:
            self.public_key = Token.generate_key()
        super().save(**kwargs)

    class Meta:
        unique_together = ('account', 'name')
        verbose_name = _('environment')
        verbose_name_plural = _('environments')
