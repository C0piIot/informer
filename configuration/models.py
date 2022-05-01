from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class Account(models.Model):
	name = models.CharField(_('name'), max_length=50)

	def __str__(self):
		return self.name


class Environment(models.Model):
	account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_('account'), editable=False)
	name = models.CharField(_('name'), max_length=50, unique=True)
	slug = models.SlugField(_('slug'), editable=False)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super().save(**kwargs)


class Channel(models.Model):
	account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=_('account'), editable=False)
	name = models.CharField(_('name'), max_length=100)
	enabled = models.BooleanField(_('enabled'), default=True)

	class Meta:
		abstract = True
		ordering = ('account', 'name',)
		verbose_name = _('channel')
		verbose_name_plural = _('channels')
		unique_together = ('account', 'name')

	def __str__(self):
		return self.name


class EmailChannel(Channel):
	host = models.CharField(_('host'), max_length=100)
	port = models.PositiveSmallIntegerField(_('port'))
	username = models.CharField(_('username'), max_length=150)
	password = models.CharField(_('password'), max_length=150)

	class Meta:
		verbose_name = _('email channel')
		verbose_name_plural = _('email channels')