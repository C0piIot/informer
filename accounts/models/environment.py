from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class Environment(models.Model):
    class Meta:
        unique_together = ("site", "name")
        verbose_name = _("environment")
        verbose_name_plural = _("environments")

    site = models.ForeignKey(
        Site,
        verbose_name=_("site"),
        on_delete=models.CASCADE,
        related_name="environments",
        editable=False,
    )
    name = models.CharField(_("name"), max_length=50)
    slug = models.SlugField(_("slug"), editable=False)
    private_key = models.CharField(_("private key"), max_length=40)
    public_key = models.CharField(_("public key"), max_length=40)

    def get_absolute_url(self):
        return reverse("stats:dashboard", kwargs={"environment": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.private_key:
            self.private_key = Token.generate_key()
        if not self.public_key:
            self.public_key = Token.generate_key()
        super().save(**kwargs)

    def __str__(self):
        return self.name
