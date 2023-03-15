from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy as _


class Channel(models.Model):
    class Meta:
        ordering = (
            "site",
            "content_type",
        )
        verbose_name = _("channel")
        verbose_name_plural = _("channels")
        unique_together = (
            "site",
            "content_type",
        )

    ICON = "🔊"
    CONTACT_FORM = None
    CONTACT_SERIALIZER = None
    CONFIG_FORM = None
    site = models.ForeignKey(
        Site, verbose_name=_("site"), on_delete=models.CASCADE, related_name="channels"
    )
    enabled = models.BooleanField(_("enabled"), default=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, editable=False
    )

    def get_typed_instance(self):
        return getattr(self, self.content_type.model)

    def save(self, *args, **kwargs):
        if not self.content_type_id:
            content_type = ContentType.objects.get_for_model(
                self, for_concrete_model=True
            )
            if content_type.model_class() != Channel:
                self.content_type = content_type
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_typed_instance().ICON} {self.content_type.name}"
