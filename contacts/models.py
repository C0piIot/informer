from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class Contact(models.Model):
    class Meta:
        verbose_name = _("contact")
        verbose_name_plural = _("contacts")
        constraints = (
            models.UniqueConstraint("environment", "key", name="key_environment"),
        )
        indexes = (
            models.Index(fields=("environment", "index1")),
            models.Index(fields=("environment", "index2")),
            models.Index(fields=("environment", "index3")),
            models.Index(fields=("environment", "index4")),
            models.Index(fields=("environment", "index5")),
            models.Index(fields=("environment", "index6")),
        )

    key = models.SlugField(
        _("key"),
        max_length=100,
        help_text=_("Id must be unique to all contacts for this environment"),
    )
    name = models.CharField(
        _("name"),
        max_length=200,
        help_text=_("This name will be used across informer app"),
    )
    site = models.ForeignKey(
        Site,
        verbose_name=_("site"),
        on_delete=models.CASCADE,
        related_name="+",
        editable=False,
    )
    environment = models.ForeignKey(
        "accounts.Environment",
        on_delete=models.CASCADE,
        verbose_name=_("environment"),
        related_name="+",
        editable=False,
    )
    index1 = models.CharField(_("index 1"), max_length=100, blank=True)
    index2 = models.CharField(_("index 2"), max_length=100, blank=True)
    index3 = models.CharField(_("index 3"), max_length=100, blank=True)
    index4 = models.CharField(_("index 4"), max_length=100, blank=True)
    index5 = models.CharField(_("index 5"), max_length=100, blank=True)
    index6 = models.CharField(_("index 6"), max_length=100, blank=True)
    contact_data = models.JSONField(
        _("contact data"),
        default=dict,
        help_text=_("Contact data will be available for use in flow templates"),
        blank=True,
    )
    channel_data = models.JSONField(_("channel data"), default=dict)
    auth_key = models.CharField(_("auth key"), max_length=40)

    def save(self, *args, **kwargs):
        self.site = self.environment.site
        if not self.auth_key:
            self.auth_key = Token.generate_key()
        super().save(*args, **kwargs)

    def set_channel_data(self, channel_type, data):
        self.channel_data[channel_type] = data

    def get_channel_data(self, channel_type):
        return self.channel_data.get(channel_type, {})

    def __str__(self):
        return self.name


class RelatedContactModel(models.Model):
    class Meta:
        abstract = True

    _contact = None
    contact_key = models.CharField(_("contact key"), max_length=100)
    environment = models.ForeignKey(
        "accounts.Environment",
        on_delete=models.CASCADE,
        verbose_name=_("environment"),
        related_name="+",
        editable=False,
    )
    site = models.ForeignKey(
        Site,
        verbose_name=_("site"),
        on_delete=models.CASCADE,
        related_name="+",
        editable=False,
    )

    @property
    def contact(self):
        if self._contact is None:
            self._contact = import_string(settings.CONTACT_STORAGE).get_contact(
                self.environment, self.contact_key
            )
        return self._contact

    @contact.setter
    def contact(self, new_contact):
        self._contact = new_contact
        self.contact_key = new_contact.key
        self.environment = new_contact.environment
        self.site = new_contact.site
