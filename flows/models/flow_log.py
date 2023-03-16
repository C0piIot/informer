from uuid import uuid4

from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy as _


class FlowLog(models.Model):
    class Meta:
        verbose_name = _("flow log")
        verbose_name_plural = _("flow logs")
        ordering = ("date",)
        indexes = (models.Index(fields=("flow_run_id", "-date")),)

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

    LEVEL_CHOICES = (
        (DEBUG, _("debug")),
        (INFO, _("info")),
        (WARNING, _("warning")),
        (ERROR, _("error")),
    )

    id = models.UUIDField(_("id"), default=uuid4,
                          primary_key=True, editable=False)
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
    flow_run_id = models.UUIDField(_("flow_run_id"))
    date = models.DateTimeField(_("date"), auto_now_add=True)
    level = models.CharField(
        _("level"), max_length=10, default=INFO, choices=LEVEL_CHOICES
    )
    message = models.CharField(_("message"), max_length=400)
    context = models.JSONField(_("context"), default=dict)

    @classmethod
    def save_flow_log(cls, log):
        log.site = log.environment.site
        log.save()

    @classmethod
    def get_flow_logs(cls, site, flow_run_id):
        return cls.objects.filter(site=site, flow_run_id=flow_run_id)

    def __str__(self):
        return f"{self.date} {self.level} {self.message}"
