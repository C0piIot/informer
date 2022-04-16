from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class Environment(models.Model):
	name = models.CharField(_('name'), max_length=50, unique=True)
	slug = models.SlugField(_('slug'))

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super().save(**kwargs)


class Channel(models.Model):
	name = models.CharField(_('name'), max_length=100, unique=True)
	enabled = models.BooleanField(_('enabled'), default=True)

	class Meta:
		ordering = ('name',)
		verbose_name = _('channel')
		verbose_name_plural = _('channels')


	def __str__(self):
		return self.name